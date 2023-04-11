# (add this at the beginning)
[app]

title = Sound_Quality_App

# (add this line)
package.name = com.yourcompany.yourapp

# (add this line)
source.dir = .

# (add this line)
source.include_exts = py,png,jpg,kv,atlas

# (add this line)
version = 0.1

# (add this line)
requirements = kivy

# (uncomment and set this to False)
orientation = landscape

# (add this line)
fullscreen = 1

# (add this line)
android.permissions = INTERNET

# (add this line)
android.arch = arm64-v8a

# (add this line)
android.api = 29

# (add this line)
android.minapi = 21

# (add this line)
android.sdk_path = /path/to/android/sdk

# (add this line)
android.ndk_path = /path/to/android/ndk

# (add this line)
android.gradle_path = /path/to/gradle

# (add this line)
android.gradle_dependencies = 'com.android.support:appcompat-v7:21.0.3'

# (add this line)
android.signing.key_alias = keyalias

# (add this line)
android.signing.storetype = jks

# (add this line)
android.signing.storepass = storepassword

# (add this line)
android.signing.keypass = keypassword

# (add this line)
android.add_activity = com.yourcompany.yourapp.MainActivity:android:label=Your App Title

# (add this line)
android.add_meta_data = android:name=android.max_aspect:resource=@integer/aspect_ratio,android:value=2.1

# (add this line)
android.add_gradle_plugin = com.android.application

# (add this line)
android.add_gradle_plugin = com.android.application

# (add this line)
android.gradle_dependencies = 'com.android.support:appcompat-v7:21.0.3'
