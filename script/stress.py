#!/usr/bin/python
# coding:utf-8

from devicewrapper.android import device as d
import unittest
import string
import time
import util
import random

a  = util.Adb()
sm = util.SetCaptureMode()
tb = util.TouchButton()
so = util.SetOption()

#Written by XuGuanjun

PACKAGE_NAME  = 'com.intel.camera22'
ACTIVITY_NAME = PACKAGE_NAME + '/.Camera'


SD                  =['4','false']
HD                  =['5','false']
HSD                 =['5','true']
HFD                 =['6','false']
HSFD                =['6','true']
CAMERAMODE_LIST     = ['Depth Snapshot','Single','Video','Panorama','Burst','Perfect Shot']
FLASH_MODE          =['on','off','auto']
SCENE_MODE          =['auto','landscape','portrait','night','sports','night-portrait']
EXPOSURE_MODE       = ['-6','-3','0','3','6']
PICTURESIZE_MODE    =['WideScreen','StandardScreen']
VIDEOSIZE_MODE      = [['false','4'],['false','5'],['true','5'],['false','6'],['true','6']]

# PATH
PATH ='/data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml '
# key
PICTURE_SIZE_KEY ='| grep pref_camera_picture_size_key'

class CameraTest(unittest.TestCase):
    def setUp(self):
        super(CameraTest,self).setUp()
        #Delete all image/video files captured before
        a.cmd('rm','/sdcard/DCIM/*')
        #Refresh media after delete files
        a.cmd('refresh','/sdcard/DCIM/*')
        #Launch social camera
        self._launchCamera()

    def tearDown(self):
        #ad.cmd('pm','com.intel.camera22') #Force reset the camera settings to default
        self._pressBack(4)
        super(CameraTest,self).tearDown()
        a.cmd('pm','com.intel.camera22')
    
    # Test case 1
    def testSwitchMode50Times(self):
        """
        Summary:testswitchmode50times: test switch mode 50 times
        Steps:  
        1.Launch single capture activity
        2.Switch camera mode 50 times
        3.Exit  activity
        """
        sm.switchCaptureMode('Single')
        for i in range(50):
            mode = random.choice(CAMERAMODE_LIST)
            sm.switchCaptureMode(mode)

        # Test case 2
    def testLaunchCamera50Times(self):
        """
        Summary:testlaunchcamera50times: Launch camera 50 times
        Steps:  
        1.Launch single capture activity
        2.Repeat 50 times
        3.Exit  activity
        """
        sm.switchCaptureMode('Single')
        for i in range(50):
            self._pressBack(4)
            a.cmd('launch','com.intel.camera22/.Camera')
            assert d(resourceId = 'com.intel.camera22:id/shutter_button').wait.exists(timeout=1000),'Launch camera failed!!'

    # Test case 3
    def testSwitchBackFrontCameraInSingleMode30Times(self):
        """
        Summary:SwitchBack/Frontcamerainsinglemode30times: Switch Back/Front camera in each mode 30 times
        Steps:  
        1.Launch single capture activity
        2.Switch Back/Front camera in single mode 30 times
        3.Exit  activity
        """
        sm.switchCaptureMode('Single')
        for i in range(30):
            tb.switchBackOrFrontCamera('front')
            tb.switchBackOrFrontCamera('back')
            time.sleep(1)

    # Test case 4
    def testChangeFlashMode100Times(self):
        """
        Summary:testChangeflashmode100times: Change flash mode 100 times
        Steps:  
        1.Launch single capture activity
        2.Change flash mode 100 times
        3.Exit  activity
        """
        sm.switchCaptureMode('Single')
        for i in range(100):
            flash_mode = random.choice(FLASH_MODE)
            so.setCameraOption('Flash',flash_mode)

    # Test case 5
    def testChangeSceneMode100Times(self):
        """
        Summary:testChangescenemode100times: Change scene mode 100 times
        Steps:  
        1.Launch single capture activity
        2.Change scene mode 100 times
        3.Exit  activity
        """
        sm.switchCaptureMode('Single')
        for i in range(100):
            scene_mode = random.choice(SCENE_MODE)
            so.setCameraOption('Scenes',scene_mode)

    # Test case 6
    def testChangeExposureMode100Times(self):
        """
        Summary:testChangeexposuremode100times: Change exposure mode 100 times
        Steps:  
        1.Launch single capture activity
        2.Change exposure mode 100 times
        3.Exit  activity
        """
        sm.switchCaptureMode('Single')
        for i in range(100):
            exposure_mode = random.choice(EXPOSURE_MODE)
            so.setCameraOption('Exposure',exposure_mode)



    # Test case 7
    def testChangePictureSizeMode100Times(self):
        """
        Summary:testChangepicturesizemode100times: Change picture size mode 100 times
        Steps:  
        1.Launch single capture activity
        2.Change picture size 100 times
        3.Exit  activity
        """
        sm.switchCaptureMode('Single')
        for i in range(100):
            size_mode = random.choice(PICTURESIZE_MODE)
            so.setCameraOption('Picture Size',size_mode)

    #Test case 8
    def testChangeVideoSizeMode100Times(self):
        """
        Summary:testChangevideosizemode100times: Change video size mode 100 times
        Steps:  
        1.Launch single capture activity
        2.Change video size 100 times
        3.Exit  activity
        """
        sm.switchCaptureMode('Single')
        sm.switchCaptureMode('Video')
        for i in range(100):
            size_mode = random.choice(VIDEOSIZE_MODE)
            so.setCameraOption('Video Size',size_mode)


    #case 9
    def testEnterGalleryFromGalleryPreviewThumbnail100times(self):
        '''
        Summary: enter gallery from gallery preview thumbnail 100times
        Steps  : 1.Launch single capture activity
                 2.enter gallery from gallery preview thumbnail 100times
                 3.Exit  activity
        '''
        sm.switchCaptureMode('Single')
        for i in range(100):
            time.sleep(3)
            tb.captureAndCheckPicCount('single',2)  # capture picture
            time.sleep(1)                                    
            d(resourceId = 'com.intel.camera22:id/thumbnail').click.wait()   # enter gallery
            time.sleep(2)
            # step 2
            d.click(1200,800)
            time.sleep(1)
            assert d(resourceId = 'android:id/home').wait.exists(timeout = 3000)
            self._pressBack(1)



    #case 10
    def testCaptureSingleImage500timesBackCamera(self):
        '''
        Summary: Capture single image 500 times
        Steps  : 1.Launch single capture activity
                 2.Capture single image 500 times
                 3.Exit  activity
        '''
        sm.switchCaptureMode('Single')
        for i in range(500):
            tb.captureAndCheckPicCount('single',2)

    #case 11
    def testCaptureSingleImage500timesFrontCamera(self):
        '''
        Summary: Capture single image 500 times
        Steps  : 1.Launch single capture activity
                 2.Capture single image 500 times
                 3.Exit  activity
        '''
        sm.switchCaptureMode('Single')
        tb.switchBackOrFrontCamera('front') #Force set camera to front
        for i in range(500):
            tb.captureAndCheckPicCount('single',2)
        tb.switchBackOrFrontCamera('back')
    
    #case 12
    def testCaptureHdrImage500timesBackCamera(self):
        '''
        Summary: Capture hdr image 500 times
        Steps  : 1.Launch hdr capture activity
                 2.Capture hdr image 500 times
                 3.Exit  activity
        '''
        sm.switchCaptureMode('Single','HDR')
        for i in range(500):
            tb.captureAndCheckPicCount('single',5)

    #case 13
    def testCaptureSmileImage500timesBackCamera(self):
        '''
        Summary: Capture smile image 500 times
        Steps  : 1.Launch smile capture activity
                 2.Capture smile image 500 times
                 3.Exit  activity
        '''
        sm.switchCaptureMode('Single','Smile')
        for i in range(500):
            tb.captureAndCheckPicCount('smile',2)

    #case 14
    def testRecord1080PVideo500times(self):
        '''
        Summary: test Record 1080P video 500 times
        Steps  : 1.Launch video capture activity
                 2.Record 1080P video 500 times
                 3.Exit  activity
        '''
        sm.switchCaptureMode('Video')
        for i in range(500):
            tb.captureAndCheckPicCount('video',5)

    #case 15
    def testRecordVideo500timesFrontCamera(self):
        '''
        Summary: test Record video 500 times
        Steps  : 1.Launch video capture activity
                 2.Change to front camera
                 3.Record video 500 times
                 4.Exit  activity
        '''
        sm.switchCaptureMode('Video')
        tb.switchBackOrFrontCamera('front')
        for i in range(500):
            tb.captureAndCheckPicCount('video',5)
        tb.switchBackOrFrontCamera('back')

    # Test case 18
    def testCapturePerectshotImage200TimesBackCamera(self):
        """
        Summary:testCaptureperfectshotimage200times: Capture perfect shot image 200 times
        Steps:  1.Launch perfectshot capture activity
                2.Capture perfectshot image 200 times
                3.Exit  activity
        """
    #step 1
        sm.switchCaptureMode('Perfect Shot')
    #step 2 
        for i in range(200):
            tb.captureAndCheckPicCount('single',5)
            time.sleep(2)


    # Test case 19
    def testCapturePanoramaImage200TimesBackCamera(self):
        """
        Summary:testCapturepanoramaimage200times: Capture panorama image 200 times
        Steps:  1.Launch panorama capture activity
                2.Capture panorama image 200 times
                3.Exit  activity
        """
    #step 1
        sm.switchCaptureMode('Panorama')
    #step 2
        for i in range(200):
            tb.captureAndCheckPicCount('smile',3)
            time.sleep(1)



    # Test case 20
    def testCaptureSingleImage8M500TimesBackCamera(self):
        """
        capture single image 500 times
        8M pixels, back camera

        """
    #step 1
        sm.switchCaptureMode('Single')
        so.setCameraOption('Picture Size','StandardScreen')
    #step 2
        tb.switchBackOrFrontCamera('back')
    #step 3
        for i in range(500):
            tb.captureAndCheckPicCount('single',3)
            time.sleep(1)
  


    # Test case 21
    def testcaseCaptureSmileImage8M500TimesBackCamera(self):
        """
        Capture Smile Image 8M 500 times back camera
        8M pixels, back camera
        """
    #step 1
        sm.switchCaptureMode('Single','Smile')
        so.setCameraOption('Picture Size','StandardScreen')
    #step 2
        tb.switchBackOrFrontCamera('back')
    #step 3
        for i in range(500):
            tb.captureAndCheckPicCount('smile',3)
            time.sleep(1)


    # Test Case 22
    def testcaseRecord720PVideo500Times(self):

        """
        Record 720P Video 500times
        Video size 720P
        """
    #step 1
        sm.switchCaptureMode('Video')
        so.setCameraOption('Video Size',['false','5'])
    #step 2 
        for i in range (500):
            tb.captureAndCheckPicCount('video',3)
            time.sleep(1)   


    # Test Case 23
    def testcaseRecord480PVideo500Times(self):
        """
        test case Record 480 Pvideo 500 times
        Video size 480P

        """
    #step 1
        sm.switchCaptureMode('Video')
        so.setCameraOption('Video Size',['false','4'])
    #step 2 
        for i in range (500):
            tb.captureAndCheckPicCount('video',3)
            time.sleep(1)   


    # Test Case 24
    def testcaseBurstImage8M200Times(self):
        """
        test case Burst Image 200 times
        8M pixels, back camera
        """

    #step 1
        sm.switchCaptureMode('Burst','Fast')
        so.setCameraOption('Picture Size','StandardScreen')
    #step 2 
        tb.switchBackOrFrontCamera('back')
    #step 3
        for i in range(200):
            tb.captureAndCheckPicCount('single',5)
            time.sleep(1)
            
    # Test Case 25
    def testCaptureDepthImage500Times(self):
        """
        test case Depth Image 500 times
        back camera
        """

    #step 1
        sm.switchCaptureMode('Depth Snapshot')
        time.sleep(10)
    #step 2
        for i in range(500):
            tb.captureAndCheckPicCount('single',2)
            time.sleep(1)

    # Test Case 26
    def testSwitchDepthToSingle100Times(self):
        """
        test Switch Depth mode to Single mode 100 times
        back camera
        """
        for i in range(100):
            sm.switchCaptureMode('Depth Snapshot')
            time.sleep(10)
            sm.switchCaptureMode('Single')
            time.sleep(2)

    # Test Case 27
    def testCaptureDepthImageThenHDRImage100Times(self):
        """
        test capture depth image and then capture HDR image 100 times.
        back camera
        """
        for i in range(100):
            sm.switchCaptureMode('Depth Snapshot')
            time.sleep(10)
            tb.captureAndCheckPicCount('single',2)
            sm.switchCaptureMode('Single','HDR')
            tb.captureAndCheckPicCount('single',2)
            time.sleep(2)

    # Test Case 28
    def testCaptureDepthImageThenSmileImage100Times(self):
        """
        test capture depth image and then capture smile image 100 times.
        back camera
        """
        for i in range(100):
            sm.switchCaptureMode('Depth Snapshot')
            time.sleep(10)
            tb.captureAndCheckPicCount('single',2)
            sm.switchCaptureMode('Single','Smile')
            tb.captureAndCheckPicCount('smile',2)
            time.sleep(2)

    # Test Case 29
    def testCaptureDepthImageThenTakeVideo100Times(self):
        """
        test capture depth image and then take video 100 times.
        back camera
        """
        for i in range(100):
            sm.switchCaptureMode('Depth Snapshot')
            time.sleep(10)
            tb.captureAndCheckPicCount('single',2)
            sm.switchCaptureMode('Video')
            tb.captureAndCheckPicCount('video',3)
            time.sleep(2)

    # Test Case 30
    def testCaptureDepthImageThenBurstImage100Times(self):
        """
        test capture depth image and then capture burst image 100 times.
        back camera
        """
        for i in range(100):
            sm.switchCaptureMode('Depth Snapshot')
            time.sleep(10)
            tb.captureAndCheckPicCount('single',2)
            sm.switchCaptureMode('Burst','Fast')
            tb.captureAndCheckPicCount('single',2)
            time.sleep(2)

    # Test Case 31
    def testCaptureDepthImageThenPanoramaImage100Times(self):
        """
        test capture depth image and then capture panorama image 100 times.
        back camera
        """
        for i in range(100):
            sm.switchCaptureMode('Depth Snapshot')
            time.sleep(10)
            tb.captureAndCheckPicCount('single',2)
            sm.switchCaptureMode('Panorama')
            tb.captureAndCheckPicCount('smile',2)
            time.sleep(2)

    # Test Case 32
    def testCaptureDepthImageThenPerfectshotImage100Times(self):
        """
        test capture depth image and then capture panorama image 100 times.
        back camera
        """
        for i in range(100):
            sm.switchCaptureMode('Depth Snapshot')
            time.sleep(10)
            tb.captureAndCheckPicCount('single',2)
            sm.switchCaptureMode('Perfect Shot')
            tb.captureAndCheckPicCount('single',2)
            time.sleep(2)

    #Add on Sep 18th
    def testcaseBurstImage6M200Times(self):
        """
        test case Burst Image 200 times
        6M pixels, back camera
        """

    #step 1
        sm.switchCaptureMode('Burst','Fast')
    #step 2 
        tb.switchBackOrFrontCamera('back')
    #step 3
        for i in range(200):
            tb.captureAndCheckPicCount('single',5)
            time.sleep(1)
            
    #Add on Sep 18th
    def testCaptureContinuousImage50times(self):
        """
        test case continuous image 50 times
        """
        sm.switchCaptureMode('Single')
        tb.switchBackOrFrontCamera('back')
        for i in range(50):
            tb.captureAndCheckPicCount('longclick',3)
            time.sleep(1)

############################################################################################################
##############################################################################################################


    def _launchCamera(self):
        d.start_activity(component = ACTIVITY_NAME)
        time.sleep(2)
        #When it is the first time to launch camera there will be a dialog to ask user 'remember location', so need to check
        if d(text = 'OK').wait.exists(timeout = 2000):
            d(text = 'OK').click.wait()
        assert d(resourceId = 'com.intel.camera22:id/mode_button').wait.exists(timeout = 3000), 'Launch camera failed in 3s'

    def _pressBack(self,touchtimes=1):
        for i in range(touchtimes):
            d.press('back')

