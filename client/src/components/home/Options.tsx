import React from 'react'
import { Button, Card, List } from 'antd'
import { ChromeOutlined, HomeOutlined, TeamOutlined} from '@ant-design/icons'

const data = [
    {
        title: 'But a property',
        content: [
            {
                icon: <HomeOutlined />,
                description: "Find your place with an immersive photo experience and the most listings",
            },
        ],
    },
    {
        title: 'Sell a property',
        content: [
            {
                icon: <ChromeOutlined />,
                description: "Whenever you are, all you need is your browser to get started buying and selling properties"
            },
        ],
    },
    {
        title: 'Sell a property',
        content: [
            {
                icon: <ChromeOutlined />,
                description: "Whenever you are, all you need is your browser to get started buying and selling properties"
            },
        ],
    },
]

const Options = () => {
  return (
    <div id='options' className='block options-block grey-bg'>
      <div className="fluid-container">
        <h2 className='text-3xl text-center'>Choose an option that fits your needs</h2>
        <p className='text-center'>It is a long established fact that a reader will be distracted</p>
      </div>
      <List
        grid={{
            gutter: 16,
            xs:1,
            sm:1,
            md:3,
            lg:3,
            xl:3,
            xxl:3
        }}
        dataSource={data}
        renderItem={(item=>(
            <List.Item>
                <Card title={item.title}>
                    <p className='large'>{item.content[0].icon}</p>
                    <p>{item.content[0].description}</p>
                    <Button type='primary' size='large'>
                        <i className="fab fa-telegram-plane"></i>
                        {" "}
                        Get Started
                    </Button>
                </Card>
            </List.Item>
        ))}
      />
      
    </div>
  )
}

export default Options
