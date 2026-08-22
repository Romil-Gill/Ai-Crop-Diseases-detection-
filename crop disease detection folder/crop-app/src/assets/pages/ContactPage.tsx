import { Mail, Phone, MapPin } from "lucide-react";

const ContactPage = () => (
  <div className="container mx-auto px-4 py-12 max-w-4xl text-center">
    <h1 className="text-3xl font-bold mb-4">Contact Our Experts</h1>
    <p className="text-slate-600 mb-12">Have questions about your crop diagnosis? Reach out to our agricultural scientists.</p>
    
    <div className="grid md:grid-cols-3 gap-8">
      <div className="p-6 bg-white rounded-xl shadow-sm border">
        <Mail className="mx-auto text-emerald-600 mb-4" size={32} />
        <h3 className="font-bold">Email</h3>
        <p className="text-sm text-slate-500">support@cropguard.ai</p>
      </div>
      <div className="p-6 bg-white rounded-xl shadow-sm border">
        <Phone className="mx-auto text-emerald-600 mb-4" size={32} />
        <h3 className="font-bold">Phone</h3>
        <p className="text-sm text-slate-500">+1 (555) 000-0000</p>
      </div>
      <div className="p-6 bg-white rounded-xl shadow-sm border">
        <MapPin className="mx-auto text-emerald-600 mb-4" size={32} />
        <h3 className="font-bold">Office</h3>
        <p className="text-sm text-slate-500">Green Valley Tech Park</p>
      </div>
    </div>

    <form className="mt-12 text-left bg-white p-8 rounded-xl shadow-sm border max-w-lg mx-auto">
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Full Name</label>
        <input type="text" className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-emerald-500 outline-none" />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Message</label>
        <textarea className="w-full border rounded-lg p-2 h-32 focus:ring-2 focus:ring-emerald-500 outline-none"></textarea>
      </div>
      <button className="w-full bg-emerald-600 text-white py-3 rounded-lg font-bold hover:bg-emerald-700 transition">Send Message</button>
    </form>
  </div>
);

export default ContactPage;