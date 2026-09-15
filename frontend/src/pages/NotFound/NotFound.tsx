import PageContainer from "../../components/layout/PageContainer";
import PageHeader from "../../components/common/PageHeader";

function NotFound() {
  return (
    <PageContainer>
      <PageHeader
        eyebrow="404"
        title="Page not found."
        description="The page you're looking for doesn't exist or has been moved."
      />
    </PageContainer>
  );
}

export default NotFound;