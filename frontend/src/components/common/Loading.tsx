import "./Common.css";

interface LoadingProps {
  message?: string;
}

export default function Loading({ message = "Loading..." }: LoadingProps) {
  return (
    <div className="loading-container" role="status">
      <div className="loading-pulse" />
      <span className="loading-message">{message}</span>
    </div>
  );
}