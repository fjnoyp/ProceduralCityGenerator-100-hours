/** \file RayTracer.cpp */
#include "RayTracer.h"
#include "App.h"

RayTracer::Settings::Settings() :
    width(160),
    height(90),
    multithreaded(true),
    useTree(false) {

    # ifdef G3D_DEBUG
        // If we’re debugging, we probably don’t want threads by default
        multithreaded = false;
    # endif
}

RayTracer::Stats::Stats() :
    lights(0),
    triangles(0),
    pixels(0),
    buildTriTreeTimeMilliseconds(0),
    rayTraceTimeMilliseconds(0) {}

void RayTracer::Photon::getPosition(const Photon& p, Vector3& pos){
    pos = p.origin;
}

bool RayTracer::Photon::equals(const Photon& p, const Photon& q){
    return (p.origin == q.origin) && (p.power == q.power) && (p.direction == q.direction);
}

size_t RayTracer::Photon::hashCode(const Photon& key){
    return key.origin.hashCode() + key.power.hashCode() - key.direction.hashCode();
}

RayTracer::RayTracer() {
    m_rnd.resize(System::numCores());
    for (int i = 0; i < m_rnd.size(); ++i) {
        // Use a different seed for each and do not be threadsafe
        m_rnd[i] = shared_ptr<Random>(new Random(i, false));
    }
}

shared_ptr<RayTracer> RayTracer::create() {
    return shared_ptr<RayTracer>(new RayTracer());
}

shared_ptr<Image> RayTracer::render(const Settings& settings,
                                    const Array< shared_ptr<Surface> >& surfaceArray,
                                    const shared_ptr<LightingEnvironment>& lighting,
                                    const shared_ptr<Camera>& camera,
                                    Stats& stats) {
    
    RealTime start;

    debugAssert(notNull(lighting) && notNull(camera));
    
    // store member copies of the arguments
    // so that they can propagate inside the callbacks
    m_settings = settings;
    m_lighting = lighting;
    m_camera = camera;
    m_stats = &stats;

    stats.indirectRays = 0;
    stats.shadowRays = 0;

    // Build the TriTree
    start = System::time();
    m_triTree.setContents(surfaceArray);
    stats.buildTriTreeTimeMilliseconds = float((System::time() - start) / units::milliseconds());
    
    // Allocate the image
    m_image = Image::create(settings.width, settings.height, ImageFormat::RGB32F());

    // Create Photon Map
    if (m_settings.enablePhotonMapping){
        start = System::time();
        createPhotonMap();
        stats.buildPhotonMapMilliseconds = float((System::time() - start) / units::milliseconds());
        stats.photonMapSize = photons.size();
    }

    // Render the image
    start = System::time();
    const int numThreads = settings.multithreaded ? GThread::NUM_CORES : 1;
    traceAllPixels(numThreads);
    stats.rayTraceTimeMilliseconds = float((System::time() - start) / units::milliseconds());
    
    // Fill out other stats
    stats.triangles = m_triTree.size();
    stats.pixels = settings.width * settings.height;
    stats.lights = lighting->lightArray.size();
    stats.primaryRays = stats.pixels * settings.raysPerPixel;
    stats.totalRays = stats.primaryRays + stats.indirectRays + stats.shadowRays;

    shared_ptr<Image> temp(m_image);

    m_triTree.clear();
    photons.clear();
    
    // Reset pointers to NULL to allow garbage collection
    m_lighting.reset();
    m_camera.reset();
    m_image.reset();

    return temp;
}

void RayTracer::traceAllPixels(int numThreads) {
    //Trace the pixels concurrently
    GThread::runConcurrently2D(Point2int32(0,0), Point2int32(m_settings.width, m_settings.height), this, &RayTracer::traceOnePixel, numThreads);
}

void RayTracer::traceOnePixel(int x, int y, int threadID) {

    //used for constructing viewport
    Vector2 tmp(m_settings.width, m_settings.height);

    Ray primaryRay;

    // If one ray per pixel: (kinda debugging mode with blue color for places with no surfel hit
    if (m_settings.raysPerPixel == 1){
        //Get the primary ray from the pixel x,y
        primaryRay = m_camera->worldRay(x + 0.5f, y + 0.5f, Rect2D(tmp));
        
        //Get the first surfel hit.
        //Can't call L_i unfortunately because we want the blue background for debugging
        const shared_ptr<Surfel>& s = RayTracer::castRay(primaryRay, finf(), 0);

        //If there is a surfel hit, get the direct illumination value and apply to the pixel
        if (s){
            //Call L_scatteredDirect to get direct illumination. Invert primaryRay to get the direction for incident light
            m_image->set(Point2int32(x,y), L_o(s, -primaryRay.direction(), m_settings.recursiveBounces, *(m_rnd[threadID])));
        } else{
            //Set the pixels with no surfel hit. Include this line so we could make it a specific color for debug purposes.
            m_image->set(Point2int32(x,y), Color3(0,0,1));
        }
    } else {
        Radiance3 L(0,0,0);
        //If more than one ray, randomly generate required number of rays within the pixel
        for (int i = 0; i < m_settings.raysPerPixel; ++i){
            primaryRay = m_camera->worldRay(x + m_rnd[threadID]->uniform(), y + m_rnd[threadID]->uniform(), Rect2D(tmp));
            L += L_i(primaryRay.origin(), primaryRay.direction(), m_settings.recursiveBounces, *(m_rnd[threadID]));
        }
        m_image->set(Point2int32(x,y), L/m_settings.raysPerPixel);
    }
}

shared_ptr<Surfel> RayTracer::castRay(const Ray& ray,float maxDistance,bool anyHit) const {

    // Distance from P to X
    float distance(maxDistance);
    shared_ptr<Surfel> surfel;

    if (m_settings.useTree) {
        // Treat the triTree as a tree
        surfel = m_triTree.intersectRay(ray, distance, anyHit);
    } else {

        // Treat the triTree as an array
        Tri::Intersector intersector;
        for (int t = 0; t < m_triTree.size(); ++t) {
            const Tri& tri = m_triTree[t];
            intersector(ray, m_triTree.cpuVertexArray(), tri,
            anyHit, distance);
        }

        surfel = intersector.surfel();

    }

    return surfel;
}


Radiance3 RayTracer::L_scatteredDirect(const shared_ptr<Surfel>& surfel, const Vector3& wo, Random& rnd) const {
    
    //Downcast to universalSurfel to allow getting lambertianReflectivity (Not used now)
    const shared_ptr<UniversalSurfel>& u = dynamic_pointer_cast<UniversalSurfel>(surfel);
    debugAssertM(notNull(u), "Encountered a Surfel that was not a UniversalSurfel");
    
    Radiance3 L(0,0,0);

    //For each light, compute the scatteredRadiance and sum them
    for (int i = 0; i < m_lighting->lightArray.size(); ++i){
        const shared_ptr<Light> light(m_lighting->lightArray[i]);
        Vector3 Y = light->position().xyz();
        Vector3 X = u->position;

        //Distance from light source to surface. Compute Birandiance using this.
        Vector3 distance = Y - X;
    
        //Computes stuff necessary for visibility function
        Vector3 wi = distance.direction();
        Vector3 n = u->shadingNormal;

        //Check visibility
        if ((wi.dot(n) > 0) && (wo.dot(n) > 0) && light->inFieldOfView(distance)){
            //Casting shadow ray from light source to surfel. To avoid intersecting the original surfel, bump the light a bit
            Color3 visibility = visiblePercentage(G3D::Ray(Y,-wi), light, distance.magnitude() - 0.1);
                //Add direct ilumination when visible, multiply biranciance by partial coverage
                if (!visibility.isZero()){
                    Biradiance3 Bi = light->bulbPower()/(4.0*G3D::pi()*square(distance.magnitude())); //Unit: W/m^2
                    L += Bi * (u->finiteScatteringDensity(wi,wo)/G3D::pi()) * abs(wi.dot(n)) * visibility;
                //Commented out, used when assuming Lambertian surface
                //L += Bi * (u->lambertianReflectivity/G3D::pi()) * abs(wi.dot(n));
            }
        }   
    }
    //Set the pixel values greater than one to one.
    return L.clamp(0,1);
}

Radiance3 RayTracer::L_i(const Point3 P, const Vector3& wi, int bouncesLeft, Random& rnd) const{
    //Get the surfel hit and call L_o to compute radiance at the surfel
    shared_ptr<Surfel> surfel = castRay(G3D::Ray(P,wi).bumpedRay(0.0001), finf(), 0);
    if (surfel){
        return L_o(surfel, -wi, bouncesLeft, rnd);
    } else{
        //No surfel, return black
        return Radiance3(0,0,0);
    }
}

Radiance3 RayTracer::L_o(const shared_ptr<Surfel>& surfel, const Vector3& wo, int bouncesLeft, Random& rnd) const{
    //Start with adding emittedRadiance from the surface
    Radiance3 L = surfel->emittedRadiance(wo); //Unit: w/m^2sr

    L += L_scatteredSpecularIndirect(surfel, wo, bouncesLeft - 1, rnd);
    
    // The option to use direct illumination for photon mapping is not implemented.
    // Therefore, we don't want to compute L_scatteredDirect when photon mapping is enabled
    if (m_settings.enablePhotonMapping){
        L += L_scatteredIndirect(surfel, wo, rnd);
    } else {
        L += L_scatteredDirect(surfel, wo, rnd);
    }
    return L;
}

Radiance3 RayTracer::L_scatteredIndirect(const shared_ptr<Surfel>& surfel, const Vector3& wo, Random& rnd) const{
    Radiance3 L(0,0,0);
    float r = m_settings.gatheringDistance;
    //Find the nearby photons
    Array<Photon> intersected;
    photons.getIntersectingMembers(Sphere(surfel->position, r), intersected);
    //Cone filter constant, set to 1 now. GUI option not implemented. (To change this, we need to add a max(0,filtered value) into code
    int k = 1;
    //Added the energy photon by photon
    for (int i = 0; i < intersected.size(); ++i){
        Photon p = intersected[i];
        L += ((p.power / (G3D::pi() * r * r)) * surfel->finiteScatteringDensity(PathDirection::EYE_TO_SOURCE, -p.direction, wo)) * (1 - (p.origin - surfel->position).magnitude()/(k*r)) / (1 - 2.0/(3.0*k));
    }
    return L;
}

Radiance3 RayTracer::L_scatteredSpecularIndirect(const shared_ptr<Surfel>& surfel, const Vector3& wo, int bouncesLeft, Random& rnd) const{
    Radiance3 L(0,0,0);
    if (bouncesLeft > 0){
        G3D::UniversalSurfel::ImpulseArray impulses;

        //Downcast to universalSurfel to allow getting impulses
        const shared_ptr<UniversalSurfel>& u = dynamic_pointer_cast<UniversalSurfel>(surfel);
        debugAssertM(notNull(u), "Encountered a Surfel that was not a UniversalSurfel");
        
        //Find the impulses on the surface
        u->getImpulses(PathDirection::EYE_TO_SOURCE, wo, impulses);

        //For each impulses, recursively computed the radiance from that direction
        for (int i = 0; i < impulses.size(); ++i){
            Vector3 wi = impulses[i].direction;
            Color3 magnitude = impulses[i].magnitude;
            ++m_stats->indirectRays;
            L += L_i(surfel->position, wi, bouncesLeft - 1, rnd) * magnitude;
        }
        
        //If we enable path tracing, also cast a random ray from the surfel
        //Technically it is not SpecularIndirect. But as it is not used often, I'm going to leave it here
        if (m_settings.enablePathTracing){
            Vector3 wi = Vector3::hemiRandom(surfel->shadingNormal, rnd);
            L += L_i(surfel->position, wi, bouncesLeft - 1, rnd) * surfel->finiteScatteringDensity(wi,wo) * abs(wi.dot(surfel->shadingNormal));
        }
    }
    return L;
}

/* returns true if a point is in shadow from a light */
Color3 RayTracer::visiblePercentage(Ray ray, const shared_ptr<Light>& light, float distance) const{
    //Only computes if we are actually casting shadows
    if (m_settings.enableShadows && light->castsShadows()){
        //Increment the amount of shadow rays
        ++m_stats->shadowRays;
        //If partial coverage is enabled, we need to compute the actual percentage, otherwise just need to test visible
        if (m_settings.enablePartialCoverage){
            Color3 visibility(1,1,1);
            //the current position of shadow ray
            Point3 oldPosition = ray.origin();
            //Iterate through the surfels in between and multiply visibility by their trasmissiveness
            //Until we reach the original surface (distance <=0) or the visibility becomes 0
            while ((distance > 0) && !(visibility.clamp(0,1).isZero())){
                shared_ptr<UniversalSurfel> surfel = dynamic_pointer_cast<UniversalSurfel>(castRay(ray.bumpedRay(0.0001), distance, 0));
                //If no more surfel left, simply return
                if (!surfel){
                    return visibility;
                } else{
                    visibility *= surfel->transmissionCoefficient;
                }

                distance = distance - (surfel->position - oldPosition).magnitude();
                oldPosition = surfel->position;
                ray = Ray(oldPosition, ray.direction());
            }

            return visibility;
        } else{
            //If not doing partial coverage, just need to test visibility. Set anysurfel to 1 for faster intersection
            if(castRay(ray.bumpedRay(0.0001), distance, 1)) {
                return Color3(0,0,0);
            } else{
                return Color3(1,1,1);
            }
        }
    } else{
        //Non shadow casting always gives total visibility
        return Color3(1,1,1);
    }
}

void RayTracer::createPhotonMap(){
    int numLights = m_lighting->lightArray.size();
    photons.clear();
    //Compute the total power of lights
    Power3 totalPower(0,0,0);
    for (int i = 0; i < numLights; ++i){
        totalPower += m_lighting->lightArray[i]->emittedPower();
    }

    shared_ptr<Random> rnd = m_rnd[0];
    
    //Calculate the probability that the photon is emitted from each light
    float prob[numLights];
    prob[0] = m_lighting->lightArray[0]->emittedPower().sum() / totalPower.sum();
    for (int i = 1; i < numLights; ++i){
        prob[i] = prob[i-1] + m_lighting->lightArray[i] -> emittedPower().sum() / totalPower.sum();
    }
    
    //Randomly emit the photons from each light source
    for (int i = 0; i < m_settings.numPhotons; ++i){
        Photon p;
        float tmp = rnd->uniform();
        int j = 0;
        while (prob[j] < tmp){
            ++j;
        }
        p.origin = m_lighting->lightArray[j]->position().xyz();
        p.power = totalPower/m_settings.numPhotons;
        
        //rejection sampling to ensure the photons are emitted in the right direction for spotlights
        //directional light not supported currently
        Vector3 tmpDirection;
        do{
            tmpDirection = Vector3::random();
        } while (m_lighting->lightArray[j]->inFieldOfView(tmpDirection));
        p.direction = tmpDirection;
            
        //trace the created photon
        tracePhotons(p, m_settings.forwardDistance);
    }

    //When finish tracing all the photons, rebalance the KDTree
    photons.balance();
}

void RayTracer::tracePhotons(Photon p, int bouncesLeft){
    //Only trace the photon if more than one bounce
    if (bouncesLeft > 0){
        //Get the intersected surface
        shared_ptr<UniversalSurfel> surfel = dynamic_pointer_cast<UniversalSurfel>(castRay(G3D::Ray(p.origin,p.direction).bumpedRay(0.0001), finf(), 0));
        if (surfel){
            p.origin = surfel->position;
            //Don't store for mirror surfaces
            if (!(surfel->glossyReflectionCoefficient.nonZero() && (surfel->glossyReflectionExponent == inf()))){
                Vector3 D = p.origin -  m_camera->frame().translation;
                //if (D.length() < 10){
                    if(castRay(G3D::Ray(m_camera->frame().translation,D).bumpedRay(0.0001), D.length(), 1)) {
                        photons.insert(p);
                    }
                //}
            }
            shared_ptr<Random> rnd = m_rnd[0];
            
            Vector3 wo;
            Color3 weight;
            //scatter the photon using the method provided by G3D. Used to be a lot of lines which got deleted
            surfel->scatter(PathDirection::SOURCE_TO_EYE, -p.direction, true, *rnd, weight, wo);
            //If it scatters, continue tracing
            if (wo.magnitude() > 0){
                p.direction = wo;
                p.power *= weight;
                tracePhotons(p, bouncesLeft - 1);
            }

            rnd.reset();
        }
    }
}
