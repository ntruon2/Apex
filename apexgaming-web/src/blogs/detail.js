
import React, {useState}  from 'react'

import {ActionBtn} from './buttons'

export function ParentBlog(props){
    const {blog} = props
    return blog.parent ? <div className='row'>
    <div className='col-11 mx-auto p-3 border rounded'>
      <p className='mb-0 text-muted small'>Reblog</p>
      <Blog hideActions className={' '} blog={blog.parent} />
    </div>
    </div> : null
  }
  export function Blog(props) {
      const {blog, didReblog, hideActions} = props
      const [actionBlog, setActionBlog] = useState(props.blog ? props.blog : null)
      const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
      const path = window.location.pathname
      const match = path.match(/(?<blogid>\d+)/)
      const urlBlogId = match ? match.groups.blogid : -1
      const isDetail = `${blog.id}` === `${urlBlogId}`

      const handleLink = (event) => {
        event.preventDefault()
        window.location.href = `/${blog.id}`
      }
      const handlePerformAction = (newActionBlog, status) => {
        if (status === 200){
          setActionBlog(newActionBlog)
        } else if (status === 201) {
          if (didReblog){
            didReblog(newActionBlog)
          }
        }

      }

      return <div className={className}>
              <div>
                <p>{blog.id} - {blog.content}</p>
                <ParentBlog blog={blog} />
              </div>
          <div className='btn btn-group'>
          {(actionBlog && hideActions !== true) && <React.Fragment>
                  <ActionBtn blog={actionBlog} didPerformAction={handlePerformAction} action={{type: "like", display:"Likes"}}/>
                  <ActionBtn blog={actionBlog} didPerformAction={handlePerformAction} action={{type: "unlike", display:"Unlike"}}/>
                  <ActionBtn blog={actionBlog} didPerformAction={handlePerformAction} action={{type: "reblog", display:"Reblog"}}/>
                </React.Fragment>
          }
                  {isDetail === true ? null : <button className='btn btn-outline-primary btn-sm' onClick={handleLink}>View</button>}
                </div>

      </div>
    }
