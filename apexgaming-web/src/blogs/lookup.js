import {backendLookup} from '../lookup'

export function apiBlogCreate(newBlog, callback){
    backendLookup("POST", "/blogs/create/", callback, {content: newBlog})
  }

export function apiBlogList(callback) {
    backendLookup("GET", "/blogs/", callback)
}
