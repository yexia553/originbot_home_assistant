#include <opencv2/opencv.hpp>
#include <string>

int main() {
    cv::VideoCapture cap(0); // open the video camera no. 0

    if (!cap.isOpened()) { // 如果没有相机
        std::cout << "Cannot open the video cam" << std::endl;
        return -1;
    }

    double dWidth = cap.get(cv::640);       // get capture width
    double dHeight = cap.get(cv::480);     // get capture height
    std::cout << "Frame size : " << dWidth << " x " << dHeight << std::endl;
  
    int frame_rate = 30;   // set your desired frame rate
    auto codec = cv::VideoWriter::fourcc(*"XVID");

    time_t start = time(0);
    long vid_duration_sec = 10;
    int idx = 0;

    while (true) {
        cv::Mat frame;

        bool bSuccess = cap.read(frame);   // read a new frame from video

        if (!bSuccess) {                   //if not successful, break loop
            std::cout << "Cannot read a frame from video stream" << std::endl;
            break;
        }

         /*we’re constantly grabbing frames and checking for keypresses afterwards*/
        if (difftime(time(0), start) >= vid_duration_sec) {
            idx++;
            start = time(0);
        }

        std::string filename = "Myvideo_" + std::to_string(idx) + ".avi";
        cv::VideoWriter record(filename,
                               codec,
                               frame_rate,
                               cv::Size(dWidth, dHeight));

        if (!record.isOpened()) {
            std::cerr << "Could not write video file" << std::endl;
            return -1;
        }
        
        record.write(frame);

        char c = (char)cv::waitKey(33);
        if (c == 27) {              // Press 'esc' to stop capturing.
            break;
        }
    }

    cap.release();
    return 0;
}

// sudo apt install libopencv-dev
// g++ yourfile.cpp -o outputfile `pkg-config --cflags --libs opencv4`