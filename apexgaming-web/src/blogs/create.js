import React from 'react'
import {apiBlogCreate} from './lookup'


export function BlogCreate(props){
  const textAreaRef = React.createRef()
  const {didBlog} = props
    const handleBackendUpdate = (response, status) =>{
      if (status === 201){
        didBlog(response)
      } else {
        console.log(response)
        alert("An error occured please try again")
      }
    }

    const handleSubmit = (event) => {
      event.preventDefault()
      const newVal = textAreaRef.current.value
      // backend api request
      apiBlogCreate(newVal, handleBackendUpdate)
      textAreaRef.current.value = ''
    }
    return <div className={props.className}>
          <form onSubmit={handleSubmit}>
            <textarea ref={textAreaRef} required={true} className='form-control' name='blog'>

            </textarea>
            <button type='submit' className='btn btn-primary my-3'>Blog</button>
        </form>
  </div>
}
