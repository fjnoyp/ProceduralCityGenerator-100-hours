#ifndef RayTracer_h
#define RayTracer_h
#include <G3D/G3DAll.h>

class RayTracer : public ReferenceCountedObject {
    public:
    class Settings {
        public:
        int width;
        int height;
        int recursiveBounces;
        int raysPerPixel;
        bool multithreaded;
        bool useTree;
        bool enableShadows;
        bool enablePartialCoverage;
        bool enablePathTracing;
        bool enablePhotonMapping;
        int numPhotons;
        int forwardDistance;
        float gatheringDistance;
        Settings();
    };
    class Stats {
        public:
        int lights;
        int triangles;
        /** width x height */
        int pixels;
        mutable int primaryRays;
        mutable int indirectRays;
        mutable int shadowRays;
        mutable int totalRays;
        int photonMapSize;
        float buildPhotonMapMilliseconds;
        float buildTriTreeTimeMilliseconds;
        float rayTraceTimeMilliseconds;
        Stats();
    };

protected:
    /** The abstraction of a Photon class that stores
        the origin, direction and power of a photon
        three methods implemented to use the PointKDTree data structre */
    class Photon {
        public:
        Point3 origin;
        Vector3 direction;
        Power3 power;
        static void getPosition(const Photon& p, Vector3& pos);
        static bool equals(const Photon& p, const Photon& q);
        static size_t hashCode(const Photon& key);
    };
    typedef PointKDTree<Photon, Photon, Photon, Photon> PhotonTree;
    /** Array of random number generators so that each threadID may
    have its own without using locks. */

    Array< shared_ptr<Random> > m_rnd;

    // The following are only valid during a call to render()
    int m_testInt;
    shared_ptr<Image> m_image;
    shared_ptr<LightingEnvironment> m_lighting;
    shared_ptr<Camera> m_camera;
    Settings m_settings;
    TriTree m_triTree;
    Stats* m_stats;
    PhotonTree photons;

    RayTracer();

    /** Called from GThread::runConcurrently2D(), which is invoked
    in traceAllPixels() */
    void traceOnePixel(int x, int y, int threadID);

    /** Called from render(). Writes to m_image. */
    void traceAllPixels(int numThreads);

    /**
    \param ray The ray in world space
    \param maxDistance Don’t trace farther than this
    \param anyHit If true, return any surface hit, even if it is
    not the first
    \return The surfel hit, or NULL if none was hit
    */
    shared_ptr<Surfel> castRay(const Ray& ray, float maxDistance = finf(),bool anyHit = false) const;

    /** Computes the direct illumination of a surface
        \param surfel the surfel we want to evalutate
        \param wo outgoing ray direction (towards eye)
        \param rnd passed random generator to enable multithreading */
    Radiance3 L_scatteredDirect(const shared_ptr<Surfel>& surfel, const Vector3& wo, Random& rnd) const;
    
    /** Find the intersection of the incoming ray, from eye to source and thus computes the radiance of the ray
        Used in backward raytracing
        \param P origin of ray
        \param wi direction of ray
        \param bouncesLeft maximum number of recursions before we stop
        \param rnd passed random generator to enable multithreading */
    Radiance3 L_i(const Point3 P, const Vector3& wi, int bouncesLeft, Random& rnd) const;

    /** Computes the radiance of a surfel to return that to L_i. Considers direct, specular, emitted and indirect illuminations
        Used in backward raytracing
        \param surfel surfel we want to evaluate
        \param wo direction of outgoing ray(eye to source)
        \param bouncesLeft maximum number of recursions before we stop
        \param rnd passed random generator to enable multithreading */ 
    Radiance3 L_o(const shared_ptr<Surfel>& surfel, const Vector3& wo, int bouncesLeft, Random& rnd) const;
    
    /** Computes the radiance contribtued by indirect illumination, excluding the impulses.
        Currently only called when photon mapping is enabled, and is also taking care of the direct illumination
        \param surfel surfel we want to evaluate
        \param wo outgoing ray direction (towards eye)
        \param rnd passed random generator to enable multithreading */ 
    Radiance3 L_scatteredIndirect(const shared_ptr<Surfel>& surfel, const Vector3& wo, Random& rnd) const;
    
    /** Computes the radiance contributed by specular indirect illumination (impulses)
        \param surfel surfel we want to evaluate
        \param wo outgoing ray direction (towards eye)
        \param bouncesLeft maximum number of recursions before we stop
        \param rnd passed random generator to enable multithreading */ 
    Radiance3 L_scatteredSpecularIndirect(const shared_ptr<Surfel>& surfel, const Vector3& wo, int bouncesLeft, Random& rnd) const;
    
    /** Computes the partial coverage between a certain light source and the surfel
        When shadowcasting is disabled or the light is non shadow-casting, always return 1
        When partial coverage is disabled, return 1 if visible and 0 if not visible. */
    Color3 visiblePercentage(Ray ray, const shared_ptr<Light>& light, float distance) const;
    
    /** Creates a photon map from the settings specified in m_settings */
    void createPhotonMap();
    
    /** Trace each photons created to store them in the photon map named photons
        \param p the photon to trace
        \param bouncesLeft maximum number of forward bounces left */
    void tracePhotons(Photon p, int bouncesLeft);
    
public:

    static shared_ptr<RayTracer> create();

    /** Render the specified image */
    
    shared_ptr<Image> render (const Settings& settings, const Array< shared_ptr<Surface> >& surfaceArray, const shared_ptr<LightingEnvironment>& lighting, const shared_ptr<Camera>& camera, Stats& stats);

};

#endif
