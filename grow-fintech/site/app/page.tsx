import Nav from "@/components/Nav";
import Hero from "@/components/Hero";
import LogosBar from "@/components/LogosBar";
import Problem from "@/components/Problem";
import Services from "@/components/Services";
import Metrics from "@/components/Metrics";
import Industries from "@/components/Industries";
import Process from "@/components/Process";
import CaseStudies from "@/components/CaseStudies";
import WhoWePartnerWith from "@/components/WhoWePartnerWith";
import Testimonials from "@/components/Testimonials";
import FAQ from "@/components/FAQ";
import FinalCTA from "@/components/FinalCTA";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <>
      <Nav />
      <main>
        <Hero />
        <LogosBar />
        <Problem />
        <Services />
        <Metrics />
        <Industries />
        <Process />
        <CaseStudies />
        <WhoWePartnerWith />
        <Testimonials />
        <FAQ />
        <FinalCTA />
      </main>
      <Footer />
    </>
  );
}
