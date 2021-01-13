import 'dart:io';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
import 'package:wix_webview/constants.dart';

class InAppWebViewScreen extends StatefulWidget {
  @override
  _InAppWebViewScreenState createState() => new _InAppWebViewScreenState();
}

class _InAppWebViewScreenState extends State<InAppWebViewScreen> {
  InAppWebViewController webView;
  ContextMenu contextMenu;
  String url = "";
  double progress = 0;
  CookieManager _cookieManager = CookieManager.instance();

  @override
  void initState() {
    super.initState();

    contextMenu = ContextMenu(
        menuItems: [
          ContextMenuItem(
              androidId: 1,
              iosId: "1",
              title: "Special",
              action: () async {
                print("Menu item Special clicked!");
                print(await webView.getSelectedText());
                await webView.clearFocus();
              })
        ],
        options: ContextMenuOptions(hideDefaultSystemContextMenuItems: true),
        onCreateContextMenu: (hitTestResult) async {
          print("onCreateContextMenu");
          print(hitTestResult.extra);
          print(await webView.getSelectedText());
        },
        onHideContextMenu: () {
          print("onHideContextMenu");
        },
        onContextMenuActionItemClicked: (contextMenuItemClicked) async {
          var id = (Platform.isAndroid)
              ? contextMenuItemClicked.androidId
              : contextMenuItemClicked.iosId;
          print("onContextMenuActionItemClicked: " +
              id.toString() +
              " " +
              contextMenuItemClicked.title);
        });
  }

  @override
  void dispose() {
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Column(
          children: <Widget>[
            Expanded(
              child: Container(
                child: InAppWebView(
                  // contextMenu: contextMenu,
                  initialUrl: WEB_URL,
                  // initialFile: "assets/index.html",

                  initialHeaders: {},

                  initialOptions: InAppWebViewGroupOptions(
                    crossPlatform: InAppWebViewOptions(
                      javaScriptCanOpenWindowsAutomatically: true,
                      debuggingEnabled: true,
                      useShouldOverrideUrlLoading: true,
                      userAgent:
                          'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36',
                    ),
                    android: AndroidInAppWebViewOptions(
                      supportMultipleWindows: true,
                      clearSessionCache: false,
                      databaseEnabled: true,
                      networkAvailable: true,
                      thirdPartyCookiesEnabled: true,
                      saveFormData: true,
                    ),
                  ), //useHybridComposition: true
                  onWebViewCreated: (InAppWebViewController controller) {
                    webView = controller;
                    print("onWebViewCreated");
                  },
                  onCreateWindow: (controller, createWindowRequest) async {
                    print("onCreateWindow");

                    showDialog(
                      context: context,
                      builder: (context) {
                        return AlertDialog(
                          content: Container(
                            width: MediaQuery.of(context).size.width,
                            height: 400,
                            child: InAppWebView(
                              // Setting the windowId property is important here!
                              windowId: createWindowRequest.windowId,
                              initialOptions: InAppWebViewGroupOptions(
                                crossPlatform: InAppWebViewOptions(
                                  debuggingEnabled: true,
                                  userAgent:
                                      'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36',
                                ),
                              ),
                              onWebViewCreated:
                                  (InAppWebViewController controller) {
                                webView = controller;
                              },
                              onLoadStart: (InAppWebViewController controller,
                                  String url) {
                                print("onLoadStart popup $url");
                              },
                              onLoadStop: (InAppWebViewController controller,
                                  String url) {
                                print("onLoadStop popup $url");
                                if (url.startsWith(
                                    'https://users.wix.com/wix-sm/api/oauth2/socialLogin')) {
                                  if (Navigator.of(context).canPop()) {
                                    Navigator.of(context).pop();
                                  }
                                }
                              },
                            ),
                          ),
                        );
                      },
                    );

                    return true;
                  },
                  onLoadStart: (InAppWebViewController controller, String url) {
                    print("onLoadStart $url");
                    setState(() {
                      this.url = url;
                    });
                  },
                  shouldOverrideUrlLoading:
                      (controller, shouldOverrideUrlLoadingRequest) async {
                    var url = shouldOverrideUrlLoadingRequest.url;
                    var uri = Uri.parse(url);

                    if (![
                      "http",
                      "https",
                      "file",
                      "chrome",
                      "data",
                      "javascript",
                      "about"
                    ].contains(uri.scheme)) {
                      if (await canLaunch(url)) {
                        // Launch the App
                        await launch(
                          url,
                        );
                        // and cancel the request
                        return ShouldOverrideUrlLoadingAction.CANCEL;
                      }
                    }

                    return ShouldOverrideUrlLoadingAction.ALLOW;
                  },
                  onLoadStop:
                      (InAppWebViewController controller, String url) async {
                    print("onLoadStop $url");

                    if (!url.startsWith(
                        'https://users.wix.com/wix-sm/api/oauth2/socialLogin')) {
                      setState(() {
                        this.url = url;
                      });
                    }
                  },
                  onProgressChanged:
                      (InAppWebViewController controller, int progress) {
                    setState(() {
                      this.progress = progress / 100;
                    });
                  },
                  onUpdateVisitedHistory: (InAppWebViewController controller,
                      String url, bool androidIsReload) {
                    print("onUpdateVisitedHistory $url");
                    setState(() {
                      this.url = url;
                    });
                  },
                  onConsoleMessage: (controller, consoleMessage) {
                    print(consoleMessage);
                  },
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
