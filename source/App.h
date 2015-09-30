/**
  \file App.h

  The G3D 10.00 default starter app is configured for OpenGL 3.3 and
  relatively recent GPUs.
 */
#ifndef App_h
#define App_h
#include <G3D/G3DAll.h>
#include "RayTracer.h"

/** Application framework. */
class App : public GApp {
protected:
    RealTime                m_lastLightingChangeTime;

    //Raytracer GUI
    /** Dropdown list containing all the possible resolutions for the rendered image */
    GuiDropDownList* m_resolutionList;

    /** settings to pass to RayTracer::render */
    RayTracer::Settings m_rayTracerSettings;
    /** stats of raytracing to be passed back by RayTracer::render */
    RayTracer::Stats m_rayTracerStats;

    /** Called from onInit */
    void makeGUI();

    //Recording
    /** Count the number of frames after the recording started */
    int m_frameCount;
    /** Start raytracing and outputting video after the specified start frame */
    int m_startFrame;
    /** Stop raytracing and outputting video after the specified end frame */ 
    int m_endFrame;
    /** Flag signalling whether we are recording a video or not */
    bool m_isRecording;
    /** Filename of the video we want to save */
    String m_saveFile;
    /** Used to output video */
    shared_ptr<VideoOutput> m_video;

    //City Generation
    /** Config file used for city generation */
    String m_cityConfig;

    
 public:
    
    App(const GApp::Settings& settings = GApp::Settings());

    virtual void onInit() override;
    virtual void onAI() override;
    virtual void onNetwork() override;
    virtual void onSimulation(RealTime rdt, SimTime sdt, SimTime idt) override;
    virtual void onPose(Array<shared_ptr<Surface> >& posed3D, Array<shared_ptr<Surface2D> >& posed2D) override;

    // You can override onGraphics if you want more control over the rendering loop.
    // virtual void onGraphics(RenderDevice* rd, Array<shared_ptr<Surface> >& surface, Array<shared_ptr<Surface2D> >& surface2D) override;

    virtual void onGraphics3D(RenderDevice* rd, Array<shared_ptr<Surface> >& surface3D) override;
    virtual void onGraphics2D(RenderDevice* rd, Array<shared_ptr<Surface2D> >& surface2D) override;

    virtual bool onEvent(const GEvent& e) override;
    virtual void onUserInput(UserInput* ui) override;
    virtual void onCleanup() override;
    
    /** Sets m_endProgram to true. */
    virtual void endProgram();

    // Raytracer GUI
    /** Update things when some item in the dropdown box is selected */
    void onResolutionChange();
    /** Render a image using raytracer when the render button is clicked */
    void onRenderButton();

    //stats GUI
    static int m_lightsGui;
    static int m_trianglesGui;
    static int m_pixelsGui;
    static float m_triTreeTimeGui;
    static float m_raytraceTimeGui;

    /** Linked to the video recording GUI, when called, resets m_framecount and set m_isRecording to true, refreshes the current scene to start recordind **/
    void onVideoStart();

    /** Generate city */
    void onCityGeneration();
    
    void onBuildingTest();
};

#endif
