import React from 'react'
import About from '../components/home/About'
import Banner from '../components/home/Banner'
import Faqs from '../components/home/Faqs'
import Options from '../components/home/Options'

const Homepage = () => {
  return (
    <div className='main'>
        <Banner />
        <About />
        <Options />
        <Faqs />
    </div>
  )
}

export default Homepage
