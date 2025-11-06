#!/usr/bin/env python
# coding: utf-8

# In[1]:


import disk_objectstore as dos


# In[12]:


cont = dos.Container(folder='test')
cont.init_container(clear=True)


# In[14]:


b = b"gkdflfdjk\nabecsa\n"
added = cont.add_object(b)
added


# In[5]:


with cont.get_object_stream(added) as fhandle:
    print(fhandle.read())


# In[6]:


with cont.get_object_stream(added) as fhandle:
    for line in fhandle.readlines():
        print(line)


# In[7]:


type(fhandle)


# In[15]:


cont.pack_all_loose(compress=True)


# In[16]:


with cont.get_object_stream(added) as fhandle:
    while True:
        line = fhandle.readline() 
        if not line:
            break
        print(line)


# In[17]:


type(fhandle)

