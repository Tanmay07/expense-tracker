import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:opentelemetry/api.dart';
import 'package:opentelemetry/sdk.dart' as sdk;

final telemetryServiceProvider = Provider<TelemetryService>((ref) {
  return TelemetryService();
});

class TelemetryService {
  late final Tracer _tracer;
  late final TracerProvider _tracerProvider;

  TelemetryService() {
    _tracerProvider = sdk.TracerProviderBase();
    _tracer = _tracerProvider.getTracer('enterprise_mobile_sdk');
  }

  void logError(String message, Object error, StackTrace stackTrace) {
    // We would ideally ship this to our observability platform, avoiding PII.
    final span = _tracer.startSpan('sdk_error');
    span.setAttributes([
      Attribute.fromString('error_message', message),
      Attribute.fromString('error_type', error.runtimeType.toString()),
      // Do not log raw PII or financial data.
    ]);
    span.end();
  }

  void logFeatureUsage(String featureName) {
    final span = _tracer.startSpan('feature_usage');
    span.setAttribute(Attribute.fromString('feature', featureName));
    span.end();
  }

  void logApiLatency(String endpoint, int durationMs, int statusCode) {
    final span = _tracer.startSpan('api_latency');
    span.setAttributes([
      Attribute.fromString('endpoint', endpoint),
      Attribute.fromInt('duration_ms', durationMs),
      Attribute.fromInt('status_code', statusCode),
    ]);
    span.end();
  }
}
