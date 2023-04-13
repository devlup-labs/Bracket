import 'package:flutter/material.dart';

import 'login_page.dart';

void main() => runApp(MaterialApp(home: loginpage()));

class loginpage extends StatelessWidget {
  const loginpage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    return SafeArea(
      child: Scaffold(
        backgroundColor: Colors.pink[100],
        body: Container(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Center(
                child: Image.asset(
                  'assets/img1.jpg',
                  height: 200,
                  width: 200,
                ),
              ),
              Center(
                child: GestureDetector(
                  child: Container(
                    width: size.width * 0.7,
                    height: size.height * 0.055,
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(8.0),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      mainAxisSize: MainAxisSize.min,
                      children: <Widget>[
                        Container(
                          child: Image.asset(
                            'assets/img2.jpg',
                            height: size.height * 0.06,
                            width: size.width * 0.06,
                          ),
                        ),
                        SizedBox(
                          width: 5.0,
                        ),
                        Text(
                          'Continue with Google',
                          style: TextStyle(fontSize: 16, letterSpacing: 1.5),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
