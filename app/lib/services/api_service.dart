import 'package:http/http.dart' as http;
import 'dart:io';
import 'package:path_provider/path_provider.dart';

class ApiService {
  // Use 10.0.2.2 for Android Emulator connecting to host localhost
  // Change to your machine's local IP for physical device testing
  static const String baseUrl = 'http://10.0.2.2:8000';

  /// Upload a video, cut + transcribe + burn subtitles.
  /// Returns the local path to the downloaded processed video file.
  static Future<String> processVideo({
    required File videoFile,
    required double trimStart,
    required double trimEnd,
    String captionStyle = '',
  }) async {
    final uri = Uri.parse('$baseUrl/upload');

    final request = http.MultipartRequest('POST', uri)
      ..fields['trim_start'] = trimStart.toString()
      ..fields['trim_end'] = trimEnd.toString()
      ..fields['caption_style'] = captionStyle
      ..files.add(await http.MultipartFile.fromPath('video', videoFile.path));

    final streamedResponse = await request.send().timeout(
      const Duration(minutes: 5),
      onTimeout: () => throw Exception('Request timed out. Is the backend running?'),
    );
    final response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 200) {
      final directory = await getApplicationDocumentsDirectory();
      final filePath =
          '${directory.path}/vibe_cut_${DateTime.now().millisecondsSinceEpoch}.mp4';
      final file = File(filePath);
      await file.writeAsBytes(response.bodyBytes);
      return filePath;
    } else {
      String errorMsg = 'Server error ${response.statusCode}';
      try {
        // Try to parse JSON error message
        final body = response.body;
        if (body.contains('"error"')) {
          errorMsg = body;
        }
      } catch (_) {}
      throw Exception(errorMsg);
    }
  }

  /// Check if the backend server is reachable.
  static Future<bool> isAvailable() async {
    try {
      final response = await http
          .get(Uri.parse('$baseUrl/health'))
          .timeout(const Duration(seconds: 3));
      return response.statusCode == 200;
    } catch (_) {
      return false;
    }
  }
}
