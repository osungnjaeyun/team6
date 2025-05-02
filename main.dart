import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_database/firebase_database.dart';
import 'firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Peltier Controller',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: TempMonitorPage(),
    );
  }
}

class TempMonitorPage extends StatefulWidget {
  @override
  _TempMonitorPageState createState() => _TempMonitorPageState();
}

class _TempMonitorPageState extends State<TempMonitorPage> {
  final dbRef = FirebaseDatabase.instance.ref();
  double temperature = 0.0;
  final double threshold = 30.0;
  bool isWarning = false;

  @override
  void initState() {
    super.initState();

    dbRef.child('status/temperature').onValue.listen((event) {
      final value = event.snapshot.value;
      setState(() {
        temperature = double.tryParse(value.toString()) ?? 0.0;
      });

      if (temperature > threshold) {
        dbRef.child('status/warning').set(true);
        setState(() {
          isWarning = true;
        });
      } else {
        dbRef.child('status/warning').set(false);
        setState(() {
          isWarning = false;
        });
      }
    });
  }

  void _turnPeltierOn() {
    dbRef.child('status/peltier').set('on');
  }

  void _turnPeltierOff() {
    dbRef.child('status/peltier').set('off');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Peltier Controller')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              '현재 온도: ${temperature.toStringAsFixed(1)} °C',
              style: TextStyle(fontSize: 30),
            ),
            SizedBox(height: 20),
            isWarning
                ? Text(
              '🔥 경고: 온도 초과!',
              style: TextStyle(color: Colors.red, fontSize: 24),
            )
                : Text(
              '✅ 안전 온도입니다.',
              style: TextStyle(color: Colors.green, fontSize: 24),
            ),
            SizedBox(height: 40),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                  onPressed: _turnPeltierOn,
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
                  child: Text('ON'),
                ),
                SizedBox(width: 20),
                ElevatedButton(
                  onPressed: _turnPeltierOff,
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.grey),
                  child: Text('OFF'),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }
}
