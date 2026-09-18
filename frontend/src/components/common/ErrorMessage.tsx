import "./Common.css";

interface ErrorMessageProps {
  message?: string;
  onRetry?: () => void;
}

export default function ErrorMessage({ message = "An unexpected error occurred.", onRetry }: ErrorMessageProps) {
  return (
    <div className="error-container" role="alert">
      <p className="error-message">{message}</p>
      {onRetry && (
        <button onClick={onRetry} className="error-retry-btn">
          Try Again
        </button>
      )}
    </div>
  );
}