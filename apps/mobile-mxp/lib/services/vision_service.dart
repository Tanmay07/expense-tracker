import 'dart:io';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:image_picker/image_picker.dart';

final visionServiceProvider = Provider<VisionService>((ref) {
  return VisionService(ImagePicker());
});

class VisionService {
  final ImagePicker _picker;

  VisionService(this._picker);

  Future<File?> captureReceipt() async {
    try {
      final XFile? image = await _picker.pickImage(
        source: ImageSource.camera,
        imageQuality: 80,
        maxWidth: 1600,
        maxHeight: 1600,
      );
      
      if (image != null) {
        return File(image.path);
      }
      return null;
    } catch (e) {
      // In a real app we'd log this to Crashlytics
      return null;
    }
  }

  Future<File?> pickReceiptFromGallery() async {
    try {
      final XFile? image = await _picker.pickImage(
        source: ImageSource.gallery,
        imageQuality: 80,
      );
      
      if (image != null) {
        return File(image.path);
      }
      return null;
    } catch (e) {
      return null;
    }
  }
}
