import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import 'dart:io';
import '../services/api_service.dart';
import 'result.dart';

class TrimmingScreen extends StatefulWidget {
  final File videoFile;
  const TrimmingScreen({super.key, required this.videoFile});

  @override
  State<TrimmingScreen> createState() => _TrimmingScreenState();
}

class _TrimmingScreenState extends State<TrimmingScreen> {
  late VideoPlayerController _controller;
  double _startTrim = 0.0;
  double _endTrim = 15.0;
  double _maxDuration = 0.0;
  bool _isProcessing = false;
  String _statusMessage = '';

  @override
  void initState() {
    super.initState();
    _controller = VideoPlayerController.file(widget.videoFile)
      ..initialize().then((_) {
        setState(() {
          _maxDuration = _controller.value.duration.inSeconds.toDouble();
          if (_maxDuration > 0) {
            _endTrim = _maxDuration > 15.0 ? 15.0 : _maxDuration;
          }
        });
        _controller.play();
        _controller.setLooping(true);
      });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _processVideo() async {
    setState(() {
      _isProcessing = true;
      _statusMessage = 'Uploading to Server...';
    });

    try {
      final processedFilePath = await ApiService.processVideo(
        videoFile: widget.videoFile,
        trimStart: _startTrim,
        trimEnd: _endTrim,
        captionStyle: 'FontName=Arial,FontSize=24,PrimaryColour=&H0000FF00', // Green style example
      );

      if (mounted) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (context) => ResultScreen(videoPath: processedFilePath),
          ),
        );
      }
    } catch (e) {
      setState(() {
        _statusMessage = 'Error: $e';
      });
    } finally {
      if (mounted) setState(() => _isProcessing = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Trim & Process')),
      body: _isProcessing 
        ? Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const CircularProgressIndicator(),
                const SizedBox(height: 20),
                Text(_statusMessage),
              ],
            ),
          )
        : Column(
            children: [
              if (_controller.value.isInitialized)
                AspectRatio(
                  aspectRatio: _controller.value.aspectRatio,
                  child: VideoPlayer(_controller),
                )
              else
                const Expanded(child: Center(child: CircularProgressIndicator())),
              
              Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  children: [
                    Text('Start: ${_startTrim.toStringAsFixed(1)}s | End: ${_endTrim.toStringAsFixed(1)}s'),
                    RangeSlider(
                      values: RangeValues(_startTrim, _endTrim),
                      min: 0,
                      max: _maxDuration > 0 ? _maxDuration : 100,
                      onChanged: (values) {
                        setState(() {
                          _startTrim = values.start;
                          _endTrim = values.end;
                        });
                        _controller.seekTo(Duration(milliseconds: (values.start * 1000).toInt()));
                      },
                    ),
                    const SizedBox(height: 20),
                    ElevatedButton(
                      onPressed: _processVideo,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.deepPurpleAccent,
                        padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 15),
                      ),
                      child: const Text('Generate Vibe-Cut', style: TextStyle(color: Colors.white)),
                    ),
                  ],
                ),
              ),
            ],
          ),
    );
  }
}
