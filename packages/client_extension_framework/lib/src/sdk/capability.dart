abstract class Capability {
  /// The unique identifier of this capability (e.g., "ocr.extract_receipt")
  String get id;
  
  /// A human-readable description of what this capability does
  String get description;

  /// Defines the expected input format/schema
  Map<String, dynamic> get inputSchema;

  /// Defines the guaranteed output format/schema
  Map<String, dynamic> get outputSchema;

  /// Execute the capability with the provided input
  Future<Map<String, dynamic>> execute(Map<String, dynamic> input);
}
