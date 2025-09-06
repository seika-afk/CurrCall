import "./globals.css";


export const metadata = {
  title: "Curriculum AI",
  description: "Chat With ECE Curriculum",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className="antialiased font-kode"
      >
	  
        {children}
      </body>
    </html>
  );
}
