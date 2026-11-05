/**
 * Research-only idempotent-create retry helper.
 *
 * Adapted for PocketCode's reference folder from the capability-gated retry
 * pattern in OpenHands/software-agent-sdk. It deliberately accepts an already
 * serialized payload so both sends use exactly the same UTF-8 body and stable
 * operation ID.
 *
 * This helper is not imported by PocketCode product code. It does not provide
 * a durable outbox, execution-result reconciliation, or exactly-once effects.
 */

export interface IdempotentCreateRetryOptions {
  /** Stable caller-owned ID. Never generate a replacement after an uncertain ack. */
  operationId: string;

  /**
   * Return true only for an opaque transport failure with no HTTP response.
   * Validation, authorization, rate-limit, and other HTTP responses must be
   * classified as false by the adapter.
   */
  isTransportFailure(error: unknown): boolean;

  /**
   * Probe the exact target server and auth scope for an explicit
   * idempotent-create capability. Probe failure must resolve false or throw.
   */
  supportsIdempotentCreate(): Promise<boolean>;
}

/**
 * Send once, then retry at most once after a transport-only failure and only
 * when the same remote service explicitly advertises ID-based deduplication.
 *
 * The caller must serialize the request once and persist operationId plus the
 * exact payload before dispatch. A server capability is meaningful only for
 * the same endpoint, tenant/account, authenticated principal and protocol
 * version. The remote server must reject same-ID/different-payload conflicts.
 */
export async function sendWithIdempotentCreateRetry<TResult>(
  immutablePayloadUtf8: string,
  send: (payloadUtf8: string, operationId: string) => Promise<TResult>,
  options: IdempotentCreateRetryOptions,
): Promise<TResult> {
  if (!options.operationId.trim()) {
    throw new TypeError("operationId must be a non-empty stable identifier");
  }

  try {
    return await send(immutablePayloadUtf8, options.operationId);
  } catch (firstError) {
    let transportFailure = false;
    try {
      transportFailure = options.isTransportFailure(firstError);
    } catch {
      // A broken classifier cannot authorize a retry.
      transportFailure = false;
    }
    if (!transportFailure) {
      throw firstError;
    }

    let capabilityConfirmed = false;
    try {
      capabilityConfirmed = await options.supportsIdempotentCreate();
    } catch {
      // A failed or unavailable capability probe is not evidence of safety.
      capabilityConfirmed = false;
    }
    if (!capabilityConfirmed) {
      throw firstError;
    }

    // Exactly one retry: same string body, same stable ID, no re-serialization.
    return send(immutablePayloadUtf8, options.operationId);
  }
}
