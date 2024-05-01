
export default function Layout({ children }: { children: React.ReactNode }) {

  return (
    <div className="flex min-h-screen w-full h-full ">
      {children}
    </div>
  );
}
