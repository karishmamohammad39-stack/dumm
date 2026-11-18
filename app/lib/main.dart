import 'package:flutter/material.dart';
import 'screens/video_selection.dart';

void main() {
  runApp(const VibeCutsApp());
}

class VibeCutsApp extends StatelessWidget {
  const VibeCutsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Vibe-Cuts',
      theme: ThemeData(
        brightness: Brightness.dark,
        primarySwatch: Colors.deepPurple,
        scaffoldBackgroundColor: const Color(0xFF121212),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF1E1E1E),
          elevation: 0,
        ),
      ),
      home: const VideoSelectionScreen(),
    );
  }
}
