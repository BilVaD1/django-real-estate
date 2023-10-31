import React from 'react'
import {SearchOutlined} from '@ant-design/icons'
import { Button, Carousel } from 'antd'


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

const Banner = () => {
  return (
    <div id='banner' className='banner-section'>
        <Carousel>
            {items.map(item=> {
                return(
                    <div key={item.key} className="fluid-container">
                        <div className="content">
                            <h3>{item.title}</h3>
                            <p>{item.content}</p>
                            <div className="btn-group">
                                <Button type='primary' size='large'>Learn More...</Button>
                                <Button icon={<SearchOutlined />} size='large'>Search</Button>
                            </div>
                        </div>
                    </div>
                )
            })}
        </Carousel>
      
    </div>
  )
}

export default Banner
