import React, {useEffect, useState}  from 'react'

import {BlogCreate} from './create'
import {Blog} from './detail'
import {apiBlogDetail} from './lookup'
import {BlogsList} from './list'


export function BlogsComponent(props) {
    const [newBlogs, setNewBlogs] = useState([])
    const canBlog = props.canBlog === "false" ? false : true
    const handleNewBlog = (newBlog) =>{
      let tempNewBlogs = [...newBlogs]
      tempNewBlogs.unshift(newBlog)
      setNewBlogs(tempNewBlogs)
    }
    return <div className={props.className}>
            {canBlog === true && <BlogCreate didBlog={handleNewBlog} className='col-12 mb-3' />}
          <BlogsList newBlogs={newBlogs} {...props} />
    </div>
}


export function BlogDetailComponent(props){
  const {blogId} = props
  const [didLookup, setDidLookup] = useState(false)
  const [blog, setBlog] = useState(null)

  const handleBackendLookup = (response, status) => {
    if (status === 200) {
      setBlog(response)
    } else {
      alert("There was an error finding your blog.")
    }
  }
  useEffect(()=>{
    if (didLookup === false){

      apiBlogDetail(blogId, handleBackendLookup)
      setDidLookup(true)
    }
  }, [blogId, didLookup, setDidLookup])

  return blog === null ? null : <Blog blog={blog} className={props.className} />
 }
