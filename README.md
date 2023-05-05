# READ ME - Concert Sound Response App

This is a repository for an app that collects listener responses every 5 minutes during a concert, initially intended to be used by participants in the Hamilton Philharmonic Orchestra's Hearing Loss Studies. 

The code is written in `kivy` and is packaged for android using `buildozer`. Kivy was initially chosen because of the Kivy Launcher App and its ability to bypass compiling. However, as of April 2023, the Kivy Launcher was no longer on the Google Play Store, and `buildozer` needed to be used to build the .apk file.

[buildozer](https://buildozer.readthedocs.io/en/latest/) runs on Linux, and was run through WSL on a Windows machine using the command `sudo buildozer android debug`. This [video](https://www.youtube.com/watch?v=pzsvN3fuBA0) was indispensable in completing the project. `cmdline-tools` and `platform-tools`'s Android Debug Bridge was used; to pull python logs from an adb connected device run: `adb -s 192.168.2.26:5555 logcat *:S python`.

---

The app was written in good part by ChatGPT, who responded to the question "What information would you need to write an application in Kivy that prompts users every 5 minutes to answer two questions?"

To write an application in Kivy that prompts users every 5 minutes to answer two questions, I would need the following information:

1. The platform(s) on which the application will run (e.g. desktop, mobile, tablet).
2. The operating system(s) on which the application will run (e.g. Windows, macOS, Linux, Android, iOS).
3. The programming language that will be used to develop the application.
4. The version of Kivy that will be used to build the application.
5. The type of questions that will be asked and how the user should respond to them.
6. The format in which the answers will be stored (e.g. text, numerical, multiple choice, etc.).
7. The storage mechanism for the user's responses (e.g. local storage, remote server).
8. Any specific design requirements or preferences for the user interface.

With this information, I can proceed to design and develop an application in Kivy that meets the specified requirements.