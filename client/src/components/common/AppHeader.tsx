import React, {useState} from 'react'
import { Anchor, Button, Drawer } from 'antd'
import { Link } from 'react-router-dom'


const AppHeader = () => {
    const [visible, setVisisble] = useState(false)

    const showDrawer = () => {
        setVisisble(true)
    }

    const closeDrawer = () => {
        setVisisble(false)
    }



  return (
    <div className='fluid-container'>
        <div className="header">
            <div className="logo">
                <i className="fas fa-home fa-2x">

                </i>
                <Link to="/">Real Estate</Link>
            </div>

            <div className="mobileHidden">
                <Anchor
                    targetOffset={65}
                    direction="horizontal"
                    items={[
                    {
                        key: 'home',
                        href: '#banner',
                        title: 'Home',
                    },
                    {
                        key: 'about',
                        href: '#about',
                        title: 'About',
                    },
                    {
                        key: 'options',
                        href: '#options',
                        title: 'Options',
                    },
                    {
                        key: 'faq',
                        href: '#faq',
                        title: 'FAQ',
                    },
                    {
                        key: 'properties',
                        href: '/properties',
                        title: 'Properties',
                    },
                    ]}
                    
                />
            </div>
            <div className="mobileVisible">
                <Button type='primary' onClick={showDrawer}>
                    <i className="fas fa-bars"></i>
                </Button>
                <Drawer 
                    placement='right' 
                    closable={false} 
                    onClose={closeDrawer} 
                    open={visible}
                >
                    <Link to="/properties" className="ant-anchor-link-title">Properties</Link>
                </Drawer>
            </div>
        </div>
      
    </div>
  )
}

export default AppHeader
