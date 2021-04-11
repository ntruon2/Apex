import React, {useEffect, useState}  from 'react'

import {apiBlogCreate, apiBlogList} from './lookup'

export function BlogsComponent(props) {
    const textAreaRef = React.createRef()
    const [newBlogs, setNewBlogs] = useState([])

    const handleBackendUpdate = (response, status) =>{
      // backend api response handler
      let tempNewBlogs = [...newBlogs]
      if (status === 201){
        tempNewBlogs.unshift(response)
        setNewBlogs(tempNewBlogs)
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
            <div className='col-12 mb-3'>
              <form onSubmit={handleSubmit}>
                <textarea ref={textAreaRef} required={true} className='form-control' name='blog'>

                </textarea>
                <button type='submit' className='btn btn-primary my-3'>Blog</button>
            </form>
            </div>
        <BlogsList newBlogs={newBlogs} />
    </div>
}

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
        apiBlogList(handleBlogListLookup)
      }
    }, [blogsInit, blogsDidSet, setBlogsDidSet])
    return blogs.map((item, index)=>{
      return <Blog blog={item} className='my-5 py-5 border bg-white text-dark' key={`${index}-{item.id}`} />
    })
  }


export function ActionBtn(props) {
    const {blog, action} = props
    const [likes, setLikes] = useState(blog.likes ? blog.likes : 0)
    const [userLike, setUserLike] = useState(blog.userLike === true ? true : false)
    const className = props.className ? props.className : 'btn btn-primary btn-sm'
    const actionDisplay = action.display ? action.display : 'Action'

    const handleClick = (event) => {
      event.preventDefault()
      if (action.type === 'like') {
        if (userLike === true) {
          // perhaps i Unlike it?
          setLikes(likes - 1)
          setUserLike(false)
        } else {
          setLikes(likes + 1)
          setUserLike(true)
        }

      }
    }
    const display = action.type === 'like' ? `${likes} ${actionDisplay}` : actionDisplay
    return <button className={className} onClick={handleClick}>{display}</button>
  }

export function Blog(props) {
    const {blog} = props
    const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
    return <div className={className}>
        <p>{blog.id} - {blog.content}</p>
        <div className='btn btn-group'>
          <ActionBtn blog={blog} action={{type: "like", display:"Likes"}}/>
          <ActionBtn blog={blog} action={{type: "unlike", display:"Unlike"}}/>
          <ActionBtn blog={blog} action={{type: "repost", display:""}}/>
        </div>
    </div>
  }
