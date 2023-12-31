import {useEffect} from 'react'
import { Alert, Col, Row, Spin } from 'antd'
import { useDispatch, useSelector } from 'react-redux'
import { listProperties } from '../actions/propertyActions'

const ProperyListPage = () => {
    const dispatch = useDispatch();

    const propertiesList = useSelector((state) => state.propertiesList)

    const {loading, error, properties} = propertiesList

    useEffect(() => {
        dispatch(listProperties())
    }, [dispatch])
    
  return (
    <div className='m-36'>
      {loading ? (
        <div className="spinner">
            <Spin size='large'/>
        </div>
      ) : error ? (
        <Alert
            type='error'
            message={error}
            showIcon
            className='alert-margin--top'
        />
      ) : (
        <>
            <Row>
                <Col span={24}>
                    <h2 className='margin--top'>Our Catolog of Properties</h2>
                </Col>
                {properties.map(property => (
                    <Col key={property.id} sm={12} md={6} lg={4} xs={3}>
                        <p>{property.title}</p>
                    </Col>
                ))}
            </Row>
        </>
      )}
    </div>
  )
}

export default ProperyListPage
