/** \file App.cpp */
#include "App.h"
#include "RayTracer.h"

// Tells C++ to invoke command-line main() function even on OS X and Win32.
G3D_START_AT_MAIN();

int main(int argc, const char* argv[]) {
	{
		G3DSpecification g3dSpec;
		g3dSpec.audio = false;
		initGLG3D(g3dSpec);
	}

    GApp::Settings settings(argc, argv);

    // Change the window and other startup parameters by modifying the
    // settings class.  For example:
    settings.window.caption			= argv[0];
    //settings.window.debugContext = true;
    // Some popular resolutions:
    //   settings.window.width        = 640;  settings.window.height       = 400;
    // settings.window.width		= 1024; settings.window.height       = 768;
     settings.window.width         = 1224; settings.window.height       = 700;
    // settings.window.width        = 1500; settings.window.height       = 800;
    // settings.window.width		= OSWindow::primaryDisplayWindowSize().x; settings.window.height = OSWindow::primaryDisplayWindowSize().y;

    // Set to true for a significant performance boost if your app can't render at 60fps,
    // or if you *want* to render faster than the display.
    settings.window.asynchronous	    = true;
    settings.depthGuardBandThickness    = Vector2int16(64, 64);
    settings.colorGuardBandThickness    = Vector2int16(16, 16);
    settings.dataDir			        = FileSystem::currentDirectory();
    settings.screenshotDirectory	    = "../journal/";

    return App(settings).run();
}


App::App(const GApp::Settings& settings) : GApp(settings) {
}


// Called before the application loop begins.  Load data here and
// not in the constructor so that common exceptions will be
// automatically caught.
void App::onInit() {
    //Initialization for rayTracer
    m_rayTracerSettings.width = 1280;
    m_rayTracerSettings.height = 720;
    m_rayTracerSettings.useTree = true;
    m_rayTracerSettings.multithreaded = true;
    m_rayTracerSettings.enableShadows = true;
    m_rayTracerSettings.recursiveBounces = 5;
    m_rayTracerSettings.raysPerPixel = 1;
    m_rayTracerSettings.numPhotons = 100000;
    m_rayTracerSettings.forwardDistance = 5;
    m_rayTracerSettings.gatheringDistance = .2;

    //Initialization for Video Recorder
    m_frameCount = 0;
    m_saveFile = "test.mp4";

    //Default City Config
    m_cityConfig = "cityPlan.cfg";

    GApp::onInit();
    setFrameDuration(1.0f / 60.0f);

    // Call setScene(shared_ptr<Scene>()) or setScene(MyScene::create()) to replace
    // the default scene here.
    
    showRenderingStats      = false;

    makeGUI();
    m_lastLightingChangeTime = 0.0;
    // For higher-quality screenshots:
    // developerWindow->videoRecordDialog->setScreenShotFormat("PNG");
    // developerWindow->videoRecordDialog->setCaptureGui(false);
    developerWindow->cameraControlWindow->moveTo(Point2(developerWindow->cameraControlWindow->rect().x0(), 0));


    //CAMERA STUFF STUFF 
    
    FilmSettings filmSettings = activeCamera()->filmSettings();
    filmSettings.setNegativeToneCurve();
    activeCamera()->filmSettings().setNegativeToneCurve(); // = filmSettings; 

    loadScene(
		"scene/buildingTest" // Load something simple
         //    developerWindow->sceneEditorWindow->selectedSceneName()  // Load the first scene encountered 
        );
}

void App::makeGUI() {
    // Initialize the developer HUD (using the existing scene)
    createDeveloperHUD();
    debugWindow->setVisible(true);
    developerWindow->videoRecordDialog->setEnabled(true);

    shared_ptr<GFont> arialFont = GFont::fromFile(System::findDataFile("icon.fnt"));
    shared_ptr<GuiTheme> theme = GuiTheme::fromFile(System::findDataFile("osx-10.7.gtm"), arialFont);

    shared_ptr<GuiWindow> renderWindow = GuiWindow::create("Render Window",theme, Rect2D::xywh(20,20,250,300),GuiTheme::TOOL_WINDOW_STYLE, GuiWindow::HIDE_ON_CLOSE);

    shared_ptr<GuiWindow> makeVideoWindow = GuiWindow::create("Make Video Window",theme, Rect2D::xywh(1200,535,250,150),GuiTheme::TOOL_WINDOW_STYLE, GuiWindow::HIDE_ON_CLOSE);

    shared_ptr<GuiWindow> cityWindow = GuiWindow::create("City Window",theme, Rect2D::xywh(300,20,250,70),GuiTheme::TOOL_WINDOW_STYLE, GuiWindow::HIDE_ON_CLOSE);

   
    
    GuiPane* MainPane = renderWindow->pane();
    addWidget(renderWindow);

    GuiPane* VideoPane = makeVideoWindow->pane();
    addWidget(makeVideoWindow);

    GuiPane* CityPane = cityWindow->pane();
    addWidget(cityWindow);


    //    GuiPane* viewPane = MainPane->addPane("View", GuiTheme::ORNATE_PANE_STYLE);
    GuiPane* infoPane = MainPane->addPane("Parameters",GuiTheme::ORNATE_PANE_STYLE);

    GuiPane* statsPane = MainPane->addPane("Stats", GuiTheme::ORNATE_PANE_STYLE);
    //statsPane->setWidth(400);
    
    GuiPane* videoSettingsPane = VideoPane->addPane("Settings", GuiTheme::ORNATE_PANE_STYLE);

    GuiPane* citySettingPane = CityPane->addPane("Settings", GuiTheme::ORNATE_PANE_STYLE);

    //Raytracer Settings
    Array <GuiText> resoList("16 x 9", "160 x 90","320 x 180", "640 x 360", "1280 x 720", "1920 x 1080");
    resoList.append("2560 x 1440");
    resoList.append("3840 x 2160");
    resoList.append("5210 x 2880");
    m_resolutionList = infoPane->addDropDownList("Resolution", resoList, new int(4), GuiControl::Callback(this, &App::onResolutionChange));

    //m_resolutionList = infoPane->addDropDownList("Resolution", Array<GuiText>("16 x 9", "160 x 90","320 x 180", "640 x 360", "1280 x 720", "1920 x 1080", "2560 x 1440", "3840 x 2160", "5210 x 2880", "7680 x 4320"), new int(4), GuiControl::Callback(this, &App::onResolutionChange));
    infoPane->addNumberBox("Recursions:", &m_rayTracerSettings.recursiveBounces);
    infoPane->addNumberBox("Rays/Pixel:", &m_rayTracerSettings.raysPerPixel);
    infoPane->addCheckBox("Multithreaded", &m_rayTracerSettings.multithreaded);
    infoPane->addCheckBox("Use Tritree", &m_rayTracerSettings.useTree);
    infoPane->addCheckBox("Enable Shadows", &m_rayTracerSettings.enableShadows);
    infoPane->addCheckBox("Partial Coverage", &m_rayTracerSettings.enablePartialCoverage);
    infoPane->addCheckBox("Path Tracing", &m_rayTracerSettings.enablePathTracing);
    infoPane->addCheckBox("Photon Mapping", &m_rayTracerSettings.enablePhotonMapping);
    infoPane->addNumberBox("Total Photons", &m_rayTracerSettings.numPhotons);
    infoPane->addNumberBox("Foward Depth", &m_rayTracerSettings.forwardDistance);
    infoPane->addNumberBox("Radius", &m_rayTracerSettings.gatheringDistance);
    infoPane->addButton("RENDER", this, &App::onRenderButton);
    
    //Raytracer stats
    statsPane->moveBy(0,320);
    statsPane->addNumberBox("Lights: ", &m_rayTracerStats.lights)->setEnabled(false);
    statsPane->addNumberBox("Triangles: ", &m_rayTracerStats.triangles)->setEnabled(false);
    statsPane->addNumberBox("Pixels: ", &m_rayTracerStats.pixels)->setEnabled(false);
    statsPane->addNumberBox("BuildMap:", &m_rayTracerStats.buildPhotonMapMilliseconds)->setEnabled(false);
    statsPane->addNumberBox("BuildTree:",&m_rayTracerStats.buildTriTreeTimeMilliseconds)->setEnabled(false);
    statsPane->addNumberBox("RayTrace:",&m_rayTracerStats.rayTraceTimeMilliseconds)->setEnabled(false);
    statsPane->addNumberBox("Primary Rays:",&m_rayTracerStats.primaryRays)->setEnabled(false);
    statsPane->addNumberBox("Indirect Rays:",&m_rayTracerStats.indirectRays)->setEnabled(false);
    statsPane->addNumberBox("Shadow Rays:",&m_rayTracerStats.shadowRays)->setEnabled(false);
    statsPane->addNumberBox("Total Rays:",&m_rayTracerStats.totalRays)->setEnabled(false);
    statsPane->addNumberBox("Total Photons:",&m_rayTracerStats.photonMapSize)->setEnabled(false);


    //For video rendering
    videoSettingsPane->addNumberBox("Start Frame:", &m_startFrame, "", GuiTheme::NO_SLIDER,0,1079999);
    videoSettingsPane->addNumberBox("End Frame:", &m_endFrame, "", GuiTheme::NO_SLIDER,0,108000);
    videoSettingsPane->addTextBox("Filename:",&m_saveFile);
    videoSettingsPane->addButton("Start Recording", this, &App::onVideoStart);

    //For city generation
    citySettingPane->addTextBox("Config File:", &m_cityConfig);
    citySettingPane->addButton("Generate City", this, &App::onCityGeneration);
    citySettingPane->addButton("Building Test", this, &App::onBuildingTest);

    statsPane->pack();
    infoPane->pack();
    videoSettingsPane->pack();
    citySettingPane->pack();
}

void App::onGraphics3D(RenderDevice* rd, Array<shared_ptr<Surface> >& allSurfaces) {
    // This implementation is equivalent to the default GApp's. It is repeated here to make it
    // easy to modify rendering. If you don't require custom rendering, just delete this
    // method from your application and rely on the base class.

    // screenPrintf("Print to the screen from anywhere in a G3D program with this command.");
    
    // Check if we are recording a video using raytracer or not, if, export a frame before the preview-renderer renders on screen
    if (m_isRecording){
        
        //increase frameCount to keep track of the number of frames went through
        ++m_frameCount; 
            
        //Only record the specified frames, this facilitates rendering using multiple machines
        if ((m_frameCount >= m_startFrame) && (m_frameCount < m_endFrame)){   
            
            //Raytracing
            shared_ptr<RayTracer> r(RayTracer::create()); 
            shared_ptr<LightingEnvironment> l = shared_ptr<LightingEnvironment>(new LightingEnvironment(scene()->lightingEnvironment()));
            shared_ptr<Image> tempImg = Image::create(m_rayTracerSettings.width, m_rayTracerSettings.height, ImageFormat::RGB32F());
            tempImg = r->render(m_rayTracerSettings, GApp::m_posed3D, l, activeCamera(), m_rayTracerStats);
            
            //Create a texture and append that to the video
            shared_ptr<Texture> frameIn = Texture::fromImage("tmpBuffer", tempImg);
            shared_ptr<Texture> frameOut;

            m_film->exposeAndRender(rd, activeCamera()->filmSettings(), frameIn, frameOut);
            m_film->exposeAndRender(rd, activeCamera()->filmSettings(), frameIn);
            m_video->append(frameOut);
        }

        debugPrintf("%d \n", m_frameCount);
    
        //If we reach the last frame, commit the video and stop recording
        if (m_frameCount == m_endFrame){
            m_video->commit();
            m_isRecording = false;
        }

    }

    if (! scene()) {
        return;
    }
    m_gbuffer->setSpecification(m_gbufferSpecification);
    m_gbuffer->resize(m_framebuffer->width(), m_framebuffer->height());

    // Share the depth buffer with the forward-rendering pipeline
    m_framebuffer->set(Framebuffer::DEPTH, m_gbuffer->texture(GBuffer::Field::DEPTH_AND_STENCIL));
    m_depthPeelFramebuffer->resize(m_framebuffer->width(), m_framebuffer->height());

    Surface::AlphaMode coverageMode = Surface::ALPHA_BLEND;

    // Bind the main framebuffer
    rd->pushState(m_framebuffer); {
        rd->clear();
        rd->setProjectionAndCameraMatrix(activeCamera()->projection(), activeCamera()->frame());

        m_gbuffer->prepare(rd, activeCamera(), 0, -(float)previousSimTimeStep(), m_settings.depthGuardBandThickness, m_settings.colorGuardBandThickness);
        
        // Cull and sort
        Array<shared_ptr<Surface> > sortedVisibleSurfaces;
        Surface::cull(activeCamera()->frame(), activeCamera()->projection(), rd->viewport(), allSurfaces, sortedVisibleSurfaces);
        Surface::sortBackToFront(sortedVisibleSurfaces, activeCamera()->frame().lookVector());
        
        const bool renderTransmissiveSurfaces = false;

        // Intentionally copy the lighting environment for mutation
        LightingEnvironment environment = scene()->lightingEnvironment();
        environment.ambientOcclusion = m_ambientOcclusion;
       
        // Render z-prepass and G-buffer.
        Surface::renderIntoGBuffer(rd, sortedVisibleSurfaces, m_gbuffer, activeCamera()->previousFrame(), activeCamera()->expressivePreviousFrame(), renderTransmissiveSurfaces, coverageMode);

        // This could be the OR of several flags; the starter begins with only one motivating algorithm for depth peel
        const bool needDepthPeel = environment.ambientOcclusionSettings.useDepthPeelBuffer;
        if (needDepthPeel) {
            rd->pushState(m_depthPeelFramebuffer); {
                rd->clear();
                rd->setProjectionAndCameraMatrix(activeCamera()->projection(), activeCamera()->frame());
                Surface::renderDepthOnly(rd, sortedVisibleSurfaces, CullFace::BACK, renderTransmissiveSurfaces, coverageMode, m_framebuffer->texture(Framebuffer::DEPTH), environment.ambientOcclusionSettings.depthPeelSeparationHint);
            } rd->popState();
        }

        if (! m_settings.colorGuardBandThickness.isZero()) {
            rd->setGuardBandClip2D(m_settings.colorGuardBandThickness);
        }        

        // Compute AO
        m_ambientOcclusion->update(rd, environment.ambientOcclusionSettings, activeCamera(), m_framebuffer->texture(Framebuffer::DEPTH), m_depthPeelFramebuffer->texture(Framebuffer::DEPTH), m_gbuffer->texture(GBuffer::Field::CS_NORMAL), m_gbuffer->texture(GBuffer::Field::SS_POSITION_CHANGE), m_settings.depthGuardBandThickness - m_settings.colorGuardBandThickness);

        const RealTime lightingChangeTime = max(scene()->lastEditingTime(), max(scene()->lastLightChangeTime(), scene()->lastVisibleChangeTime()));
        bool updateShadowMaps = false;
        if (lightingChangeTime > m_lastLightingChangeTime) {
            m_lastLightingChangeTime = lightingChangeTime;
            updateShadowMaps = true;
        }
        // No need to write depth, since it was covered by the gbuffer pass
        rd->setDepthWrite(false);
        // Compute shadow maps and forward-render visible surfaces
        Surface::render(rd, activeCamera()->frame(), activeCamera()->projection(), sortedVisibleSurfaces, allSurfaces, environment, coverageMode, updateShadowMaps, m_settings.depthGuardBandThickness - m_settings.colorGuardBandThickness, sceneVisualizationSettings());      
                
        // Call to make the App show the output of debugDraw(...)
        drawDebugShapes();
        const shared_ptr<Entity>& selectedEntity = (notNull(developerWindow) && notNull(developerWindow->sceneEditorWindow)) ? developerWindow->sceneEditorWindow->selectedEntity() : shared_ptr<Entity>();
        scene()->visualize(rd, selectedEntity, sceneVisualizationSettings());

        // Post-process special effects
        m_depthOfField->apply(rd, m_framebuffer->texture(0), m_framebuffer->texture(Framebuffer::DEPTH), activeCamera(), m_settings.depthGuardBandThickness - m_settings.colorGuardBandThickness);
        
        m_motionBlur->apply(rd, m_framebuffer->texture(0), m_gbuffer->texture(GBuffer::Field::SS_EXPRESSIVE_MOTION), 
                            m_framebuffer->texture(Framebuffer::DEPTH), activeCamera(), 
                            m_settings.depthGuardBandThickness - m_settings.colorGuardBandThickness);

    } rd->popState();

    // We're about to render to the actual back buffer, so swap the buffers now.
    // This call also allows the screenshot and video recording to capture the
    // previous frame just before it is displayed.
    swapBuffers();

	// Clear the entire screen (needed even though we'll render over it, since
    // AFR uses clear() to detect that the buffer is not re-used.)
    rd->clear();

    // Perform gamma correction, bloom, and SSAA, and write to the native window frame buffer
    m_film->exposeAndRender(rd, activeCamera()->filmSettings(), m_framebuffer->texture(0));
}


void App::onAI() {
    GApp::onAI();
    // Add non-simulation game logic and AI code here
}


void App::onNetwork() {
    GApp::onNetwork();
    // Poll net messages here
}


void App::onSimulation(RealTime rdt, SimTime sdt, SimTime idt) {
    GApp::onSimulation(rdt, sdt, idt);

    // Example GUI dynamic layout code.  Resize the debugWindow to fill
    // the screen horizontally.
    debugWindow->setRect(Rect2D::xywh(0, 0, (float)window()->width(), debugWindow->rect().height()));
}


bool App::onEvent(const GEvent& event) {
    // Handle super-class events
    if (GApp::onEvent(event)) { return true; }

    // If you need to track individual UI events, manage them here.
    // Return true if you want to prevent other parts of the system
    // from observing this specific event.
    //
    // For example,
    // if ((event.type == GEventType::GUI_ACTION) && (event.gui.control == m_button)) { ... return true; }
    // if ((event.type == GEventType::KEY_DOWN) && (event.key.keysym.sym == GKey::TAB)) { ... return true; }

    return false;
}


void App::onUserInput(UserInput* ui) {
    GApp::onUserInput(ui);
    (void)ui;
    // Add key handling here based on the keys currently held or
    // ones that changed in the last frame.
}


void App::onPose(Array<shared_ptr<Surface> >& surface, Array<shared_ptr<Surface2D> >& surface2D) {
    GApp::onPose(surface, surface2D);

    // Append any models to the arrays that you want to later be rendered by onGraphics()
}


void App::onGraphics2D(RenderDevice* rd, Array<shared_ptr<Surface2D> >& posed2D) {
    // Render 2D objects like Widgets.  These do not receive tone mapping or gamma correction.
    Surface2D::sortAndRender(rd, posed2D);
}


void App::onCleanup() {
    // Called after the application loop ends.  Place a majority of cleanup code
    // here instead of in the constructor so that exceptions can be caught.
}


void App::endProgram() {
    m_endProgram = true;
}

void App::onResolutionChange() {
    TextInput ti(TextInput::FROM_STRING,
                 m_resolutionList->selectedValue().text());
    m_rayTracerSettings.width = ti.readNumber();
    ti.readSymbol("x");
    m_rayTracerSettings.height = ti.readNumber();
}

void App::onRenderButton(){
    //Creates Raytracer
    shared_ptr<RayTracer> r(RayTracer::create()); 

    shared_ptr<LightingEnvironment> l 
        = shared_ptr<LightingEnvironment>(new LightingEnvironment(scene()->lightingEnvironment()));

    //Create image and use raytracer
    shared_ptr<Image> tempImg 
        = Image::create(m_rayTracerSettings.width, m_rayTracerSettings.height, ImageFormat::RGB32F());
    tempImg = r->render(m_rayTracerSettings, GApp::m_posed3D, l, activeCamera(), m_rayTracerStats);
        
    //Display the image
    GApp::show(tempImg, "Rendered Image");   
}

void App::onVideoStart(){
    //use resolution setting for raytracer
    VideoOutput::Settings v_settings(VideoOutput::CODEC_ID_MPEG4, m_rayTracerSettings.width, m_rayTracerSettings.height, 30.0f, 0);
    //manually increasing bitrate to ensure quality
    v_settings.bitrate = 10000000.0;
    m_video = VideoOutput::create(m_saveFile, v_settings);
    //refreshes and start recording
    GApp::loadScene(scene()->name());
    m_frameCount = 0;
    m_isRecording = true;
}

void App::onCityGeneration() {
    String args = "python city.py " + m_cityConfig;
    system(args.c_str());
    String name = scene()->name();
    //Load Empty Scene to refresh objects
    loadScene("scene/buildingTest");
    //Pause to avoid race condition
    sleep(1);
    GApp::loadScene(name);
}

void App::onBuildingTest() {
    system("python building.py");
    loadScene("G3D Cornell Box"); 
    loadScene("scene/buildingTest");
}
