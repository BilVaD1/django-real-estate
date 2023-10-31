import React from 'react'
import { Col, Row } from 'antd'


const items = [
  {
    key:'1',
    icon: <i className="fas fa-search-location"></i>,
    title:"Simplified Search",
    content:"Lorem Ipsum"
  },
  {
    key:'2',
    icon: <i className="fas fa-database"></i>,
    title:"Lot of properties",
    content:"Lorem Ipsum"
  },
  {
    key:'3',
    icon: <i className="fas fa-globe-africa"></i>,
    title:"Proudly African",
    content:"Lorem Ipsum"
  },
]

const About = () => {
  return (
    <div id="about" className='block about-section'>
      <div className="fluid-container">
        <div className="title-section">
          <h2>About us</h2>
          <p>You will find us very interesting</p>
        </div>
        <div className="content-section">
          <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod t
          empor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, 
          quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo 
          consequat. Duis aute irure dolor in reprehenderit in voluptate 
          velit esse cillum dolore eu fugiat nulla pariatur. Excepteur 
          sint occaecat cupidatat non proident, sunt in culpa qui officia 
          deserunt mollit anim id est laborum.
          </p>
        </div>
        <Row gutter={[16,16]}>
          {items.map(item=>{
            return(
              <Col md={{span: 8}} key={item.key}>
                <div className="content">
                  <div className="icon">{item.icon}</div>
                  <h3>{item.title}</h3>
                  <p>{item.content}</p>
                </div>
              </Col>
            )
          })}
        </Row>
      </div>
      
    </div>
  )
}

export default About
