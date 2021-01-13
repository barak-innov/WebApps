import 'package:flutter/material.dart';
import 'package:wix_webview/webview_screen.dart';
// import 'package:permission_handler/permission_handler.dart';

// InAppLocalhostServer localhostServer = new InAppLocalhostServer();

class InAppWebViewExample extends StatefulWidget {
  @override
  _InAppWebViewExampleState createState() => new _InAppWebViewExampleState();
}

class _InAppWebViewExampleState extends State<InAppWebViewExample> {
  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(initialRoute: '/', routes: {
      '/': (context) => InAppWebViewScreen(),
    });
  }
}

//--------------------------------------------------
