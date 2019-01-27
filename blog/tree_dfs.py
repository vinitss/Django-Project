from .models import Comment
adj=[]
ordered_comments=[]
visited=[]
def addEdge(parent,child):
    global adj
    adj[parent].append(child)

def addNode():
    global adj
    adj.append([])

def firstComment(init_pk):
    global adj
    for i in range(init_pk+1):
        adj.append([])

def dfs(s,p,spc):
    global adj
    global ordered_comments
    global visited
    ordered_comments.append([s,spc])
    visited[s]=True
    print (str(s) + "-")
    for v in adj[s]:
        if (v!=p):
            print(str(v))
            dfs(v,s,spc+1)

def dfsDisconnected(s):
    global adj
    global visited
    global ordered_comments
    ordered_comments=[]
    visited=[]
    for i in range(0,len(adj)):
        visited.append(False)
    print (len(adj)==len(visited))
    for i in range(s,len(adj)):
        if (visited[i]==False):
            print ("start " + str(i))
            dfs(i,-1,0)
    print ("in dfs")
    return (ordered_comments)

def init_graph():
    fCom=Comment.objects.first()
    deletedComments=fCom.pk-1
    #print (deletedComments)
    firstComment(deletedComments)
    comments_all=Comment.objects.all()
    for comment in comments_all:
        addNode()
        deletedComments+=1
        if (comment.parent!=None):
            parent_pk = comment.parent.pk
            child_pk = comment.pk
            addEdge(parent_pk,child_pk)
    return deletedComments
