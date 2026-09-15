type PageContainerProps = {
  children: React.ReactNode;
  className?: string;
};

function PageContainer({
  children,
  className = "",
}: PageContainerProps) {
  return (
    <div className={`container ${className}`}>
      {children}
    </div>
  );
}

export default PageContainer;