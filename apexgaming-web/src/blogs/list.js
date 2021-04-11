import React, {useEffect, useState}  from 'react'

import {apiBlogList} from './lookup'

import {Blog} from './detail'

export function BlogsList(props) {
    const [blogsInit, setBlogsInit] = useState([])
    const [blogs, setBlogs] = useState([])
    const [blogsDidSet, setBlogsDidSet] = useState(false)
    useEffect(()=>{
      const final = [...props.newBlogs].concat(blogsInit)
      if (final.length !== blogs.length) {
        setBlogs(final)
      }
    }, [props.newBlogs, blogs, blogsInit])

    useEffect(() => {
      if (blogsDidSet === false){
        const handleBlogListLookup = (response, status) => {
          if (status === 200){
            setBlogsInit(response)
            setBlogsDidSet(true)
          } else {
            alert("There was an error")
          }
        }
        apiBlogList(props.username, handleBlogListLookup)
      }
    }, [blogsInit, blogsDidSet, setBlogsDidSet, props.username])


    const handleDidReblog = (newBlog) => {
      const updateBlogsInit = [...blogsInit]
      updateBlogsInit.unshift(newBlog)
      setBlogsInit(updateBlogsInit)
      const updateFinalBlogs = [...blogs]
      updateFinalBlogs.unshift(blogs)
      setBlogs(updateFinalBlogs)
    }
    return blogs.map((item, index)=>{
      return <Blog
        blog={item}
        didReblog={handleDidReblog}
        className='my-5 py-5 border bg-white text-dark'
        key={`${index}-{item.id}`} />
    })
  }
