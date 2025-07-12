import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Search, Home, DollarSign, Users, Star, Phone, Mail, MapPin } from 'lucide-react'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('buy')
  const [searchKeyword, setSearchKeyword] = useState('')

  const testimonials = [
    {
      name: "Claude and Vivian Banks",
      text: "Our Revolution Realty Agent didn't try to push any old house on us, and readily pointed out issues during home tours that we might have overlooked",
      image: "/api/placeholder/400/300"
    }
  ]

  const blogPosts = [
    {
      title: "Home Buying Tips for First-Time Buyers",
      date: "Dec 15th 2024",
      teaser: "Essential tips and tricks for navigating your first home purchase.",
      image: "/api/placeholder/300/200"
    },
    {
      title: "Market Trends in Cedar Rapids",
      date: "Dec 10th 2024", 
      teaser: "Latest market analysis and trends in the Cedar Rapids area.",
      image: "/api/placeholder/300/200"
    },
    {
      title: "Selling Your Home for Top Dollar",
      date: "Dec 5th 2024",
      teaser: "Strategies to maximize your home's value in today's market.",
      image: "/api/placeholder/300/200"
    },
    {
      title: "Investment Properties Guide",
      date: "Nov 30th 2024",
      teaser: "How to identify and invest in profitable real estate.",
      image: "/api/placeholder/300/200"
    }
  ]

  const features = {
    buy: [
      {
        title: "Find Your Dream Home",
        description: "Search through thousands of listings to find the perfect home for you and your family.",
        icon: <Home className="w-8 h-8" />
      },
      {
        title: "Expert Guidance",
        description: "Our experienced agents will guide you through every step of the buying process.",
        icon: <Users className="w-8 h-8" />
      },
      {
        title: "Market Analysis",
        description: "Get detailed market analysis and pricing information for informed decisions.",
        icon: <DollarSign className="w-8 h-8" />
      }
    ],
    sell: [
      {
        title: "Sell for 5%",
        description: "List your home with us and save on commission fees with our competitive 5% rate.",
        icon: <DollarSign className="w-8 h-8" />
      },
      {
        title: "Professional Marketing",
        description: "Professional photography, online listings, and marketing to reach qualified buyers.",
        icon: <Star className="w-8 h-8" />
      },
      {
        title: "Quick Sales",
        description: "Our proven strategies help sell homes faster than the market average.",
        icon: <Home className="w-8 h-8" />
      }
    ]
  }

  const handleSearch = (e) => {
    e.preventDefault()
    console.log('Searching for:', searchKeyword)
    // Implement search functionality
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Home className="w-8 h-8 text-primary" />
              <span className="text-2xl font-bold text-primary">Revolution Realty</span>
            </div>
            <nav className="hidden md:flex space-x-6">
              <a href="#" className="text-foreground hover:text-primary transition-colors">Buy</a>
              <a href="#" className="text-foreground hover:text-primary transition-colors">Sell</a>
              <a href="#" className="text-foreground hover:text-primary transition-colors">Agents</a>
              <a href="#" className="text-foreground hover:text-primary transition-colors">Vendors</a>
              <a href="#" className="text-foreground hover:text-primary transition-colors">Blog</a>
              <a href="#" className="text-foreground hover:text-primary transition-colors">Contact</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-blue-600 to-blue-800 text-white">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative container mx-auto px-4 py-20">
          {/* Tab Navigation */}
          <div className="flex justify-center mb-8">
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-1">
              <button
                onClick={() => setActiveTab('buy')}
                className={`px-8 py-3 rounded-md font-semibold transition-all ${
                  activeTab === 'buy' 
                    ? 'bg-white text-blue-800 shadow-lg' 
                    : 'text-white hover:bg-white/10'
                }`}
              >
                BUY
              </button>
              <button
                onClick={() => setActiveTab('sell')}
                className={`px-8 py-3 rounded-md font-semibold transition-all ${
                  activeTab === 'sell' 
                    ? 'bg-white text-blue-800 shadow-lg' 
                    : 'text-white hover:bg-white/10'
                }`}
              >
                SELL
              </button>
            </div>
          </div>

          {/* Content based on active tab */}
          {activeTab === 'buy' && (
            <div className="text-center">
              <h1 className="text-5xl font-bold mb-6">Find Your Dream Home</h1>
              <form onSubmit={handleSearch} className="max-w-2xl mx-auto mb-8">
                <div className="flex gap-2">
                  <Input
                    type="text"
                    placeholder="Enter address, city, state, zip, or keyword"
                    value={searchKeyword}
                    onChange={(e) => setSearchKeyword(e.target.value)}
                    className="flex-1 h-12 text-lg"
                  />
                  <Button type="submit" size="lg" className="h-12 px-8">
                    <Search className="w-5 h-5 mr-2" />
                    Search
                  </Button>
                </div>
                <div className="flex items-center justify-center mt-4">
                  <label className="flex items-center text-white/90">
                    <input type="checkbox" className="mr-2" />
                    Only <strong className="mx-1">Revolution Realty</strong> Properties
                  </label>
                </div>
              </form>
              <div className="text-center">
                <h2 className="text-2xl font-semibold mb-4">Start Your Home Search Today</h2>
                <Button size="lg" variant="secondary">
                  Browse Properties
                </Button>
              </div>
            </div>
          )}

          {activeTab === 'sell' && (
            <div className="text-center">
              <h1 className="text-5xl font-bold mb-6">Sell Your Home for 5%</h1>
              <form onSubmit={handleSearch} className="max-w-2xl mx-auto mb-8">
                <div className="flex gap-2">
                  <Input
                    type="text"
                    placeholder="Enter current address"
                    value={searchKeyword}
                    onChange={(e) => setSearchKeyword(e.target.value)}
                    className="flex-1 h-12 text-lg"
                  />
                  <Button type="submit" size="lg" className="h-12 px-8">
                    Go
                  </Button>
                </div>
              </form>
              <div className="text-center">
                <h2 className="text-2xl font-semibold mb-4">Get a Free Home Valuation</h2>
                <Button size="lg" variant="secondary">
                  Get Started
                </Button>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-3 gap-8">
            {features[activeTab].map((feature, index) => (
              <Card key={index} className="text-center">
                <CardHeader>
                  <div className="flex justify-center mb-4 text-primary">
                    {feature.icon}
                  </div>
                  <CardTitle>{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Interactive Section */}
      <section className="py-16 bg-gradient-to-r from-gray-800 to-gray-900 text-white">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold mb-6">Experience Virtual Tours</h2>
              <h3 className="text-xl font-semibold mb-4">Immersive 3D Home Tours</h3>
              <p className="mb-6 text-gray-300">
                Take virtual tours of properties from the comfort of your home. Our 3D technology 
                lets you explore every room and get a real feel for the space.
              </p>
              <h3 className="text-xl font-semibold mb-4">Professional Photography</h3>
              <p className="text-gray-300">
                Every listing features professional photography and detailed floor plans to help 
                you make informed decisions about your next home.
              </p>
            </div>
            <div className="bg-gray-700 rounded-lg p-8 text-center">
              <div className="w-full h-64 bg-gray-600 rounded-lg mb-4 flex items-center justify-center">
                <Home className="w-16 h-16 text-gray-400" />
              </div>
              <Button variant="secondary" size="lg">
                Start Virtual Tour
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">What Our Clients Say</h2>
          <div className="max-w-4xl mx-auto">
            {testimonials.map((testimonial, index) => (
              <Card key={index} className="mb-8">
                <CardContent className="p-8">
                  <div className="grid md:grid-cols-2 gap-8 items-center">
                    <div>
                      <p className="text-lg italic mb-4">"{testimonial.text}"</p>
                      <p className="font-semibold">- {testimonial.name}</p>
                    </div>
                    <div className="bg-gray-200 rounded-lg h-64 flex items-center justify-center">
                      <Users className="w-16 h-16 text-gray-400" />
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Blog Section */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Revolutionary <strong>Blog</strong></h2>
          </div>
          <div className="grid md:grid-cols-4 gap-6">
            {blogPosts.map((post, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow">
                <div className="bg-gray-200 h-48 rounded-t-lg flex items-center justify-center">
                  <Home className="w-12 h-12 text-gray-400" />
                </div>
                <CardHeader>
                  <CardTitle className="text-lg">{post.title}</CardTitle>
                  <CardDescription>{post.date}</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">{post.teaser}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Home className="w-6 h-6" />
                <span className="text-xl font-bold">Revolution Realty</span>
              </div>
              <p className="text-gray-400">
                Your trusted partner in buying and selling homes in Cedar Rapids, Waterloo, Marion and Eastern Iowa.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Services</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Buy a Home</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Sell Your Home</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Property Search</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Market Analysis</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Resources</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Our Agents</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Vendors</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact Us</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Contact Info</h3>
              <div className="space-y-2 text-gray-400">
                <div className="flex items-center space-x-2">
                  <Phone className="w-4 h-4" />
                  <span>(319) 555-0123</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Mail className="w-4 h-4" />
                  <span>info@revolutionrealty.com</span>
                </div>
                <div className="flex items-center space-x-2">
                  <MapPin className="w-4 h-4" />
                  <span>Cedar Rapids, IA</span>
                </div>
              </div>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Revolution Realty. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App

