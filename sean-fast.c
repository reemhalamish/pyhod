#ifdef _CH_
#pragma package <opencv>
#endif

#ifndef _EiC
#include "cv.h"
#include "highgui.h"
#include <stdio.h>
#include <ctype.h>
#endif

int vmin = 240;
int vmax = 255;

int main( int argc, char** argv )
{
    CvCapture* capture = 0;
    
    capture = cvCaptureFromCAM(0);

    if( !capture )
    {
        fprintf(stderr,"Could not initialize capturing...\n");
        return -1;
    }

    cvSetCaptureProperty(capture,CV_CAP_PROP_FRAME_WIDTH, 640);
    cvSetCaptureProperty(capture,CV_CAP_PROP_FRAME_HEIGHT, 480);


	cvNamedWindow("Camera", CV_WINDOW_AUTOSIZE);
        cvNamedWindow("Hue", CV_WINDOW_AUTOSIZE);
        cvNamedWindow("Saturation", CV_WINDOW_AUTOSIZE);
        cvNamedWindow("Value", CV_WINDOW_AUTOSIZE);
        cvNamedWindow("Laser", CV_WINDOW_AUTOSIZE);
        cvMoveWindow("Camera", 0, 10);
        cvMoveWindow("Hue", 0, 350);
        cvMoveWindow("Saturation", 360, 10);
        cvMoveWindow("Value", 360, 350);
        cvMoveWindow("Laser", 700, 40);

        IplImage* frame = 0;
    	frame = cvQueryFrame(capture);
        CvSize frameSize = cvGetSize(frame);

        IplImage *hsv = cvCreateImage(frameSize,8,3);
        IplImage *mask = cvCreateImage(frameSize,8,1);
        IplImage *hue = cvCreateImage(frameSize,8,1);
        IplImage *saturation = cvCreateImage(frameSize,8,1);
        IplImage *value = cvCreateImage(frameSize,8,1);
        IplImage *laser = cvCreateImage(frameSize,8,1);

    for(;;)
    {
        int i, bin_w, c;
        frame = cvQueryFrame( capture );
        if( !frame )
            break;

	cvCvtColor(frame,hsv,CV_BGR2HSV);
	cvSplit(hsv,hue,saturation,value,NULL);

	cvInRangeS(value,cvRealScalar(vmin),cvRealScalar(vmax),value);

        cvShowImage( "Camera", frame );
        cvShowImage( "Hue", hue );
        cvShowImage( "Saturation", saturation );
        cvShowImage( "Value", value );
        cvShowImage( "Laser", laser );

        c = cvWaitKey(70);
        if( (char) c == 27 )
            break;
    }

    cvReleaseCapture( &capture );
    cvDestroyWindow("CamShiftDemo");

    return 0;
}

#ifdef _EiC
main(1,"camshiftdemo.c");
#endif
