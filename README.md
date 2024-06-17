# Pomodoro with camera detect distracted
* First the Pomodoro Technique is a time management method developed by Francesco Cirillo in the late 1980s. It is designed to improve productivity by breaking work into intervals, traditionally 25 minutes in length, separated by short breaks. These intervals are called "pomodoros," named after the tomato-shaped kitchen timer that Cirillo used as a university student.
* To increase the effectiveness of this method applied in learning and working, I suggest use a camera to monitor user's learn or work progress by use YOLOv8 detect user's distraction.
* When camera detect user out of focus to learn or work, the time of camera will stop and user can select two option: First is do some simple exercise to improve focus and second is continue the pomodoro progress
  
## How this its work?
### 1. Time countdown of Pomodoro
* Base on Pomodoro timer, we will have 25 minutes for learning/ working, 5 minutes for a short break, and after four times learning progress it will have 15 minutes for a long break time
  
| ![image](https://github.com/n1ne1903/Pomodoro-with-camera-detect-distracted/assets/141629048/32c5e64d-b9fc-4673-8dae-ca97404ff03c) | ![image](https://github.com/n1ne1903/Pomodoro-with-camera-detect-distracted/assets/141629048/4e9fe3ee-7a88-4155-9187-08d57ba6bd7f) | ![image](https://github.com/n1ne1903/Pomodoro-with-camera-detect-distracted/assets/141629048/f158813d-6612-4343-a583-240915035202) |
|:------------------------------:|:------------------------------:|:------------------------------:|
| Start progress with 25 minutes              | Get a short break for 5 minutes             | Long break with 15 minutes after 4 times of progress            |

### 2. Camera detect distracted
* Camera use YOLOv8 to monitor your progress by dectect your face, if detect distracted, time will be paused
  
| ![image](https://github.com/n1ne1903/Pomodoro-with-camera-detect-distracted/assets/141629048/48b748aa-adc9-44bf-825c-494842b9c83c) | ![image](https://github.com/n1ne1903/Pomodoro-with-camera-detect-distracted/assets/141629048/4665ea0d-78b1-43a6-b5a4-e3b04081e415) |
|:------------------------------:|:------------------------------:|
| Boundingbox of Yolov8 to monitor user            | YOLOv8 detect user's distracted and send a massage box         |

*End of a progress it will anouce in this progress how many times do we lose focus and if you have more than 5 times in a round it will suggest you to have a long break
|![image](https://github.com/n1ne1903/Pomodoro-with-camera-detect-distracted/assets/141629048/bb3dcf11-2257-433b-b302-87f9a13ece8d)  |  ![image](https://github.com/n1ne1903/Pomodoro-with-camera-detect-distracted/assets/141629048/2dba7028-c349-476e-9b73-8c9e9337aa72) | ![image](https://github.com/n1ne1903/Pomodoro-with-camera-detect-distracted/assets/141629048/70bd48c0-aa95-4a92-9f3c-afffd32c587d) |
|:------------------------------:|:------------------------------:|:------------------------------:|
| Camera detect user have one time distracted             | Massage when u have many times distracted in a progress            | Long break time instead of short break when           |




