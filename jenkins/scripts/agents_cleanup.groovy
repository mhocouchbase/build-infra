import hudson.model.*;
import hudson.util.*;
import jenkins.model.*;
import hudson.FilePath.FileCallable;
import hudson.slaves.OfflineCause;
import hudson.node_monitors.*;

//  The main purpose of this script is to remove leftover and older
//  Jenkins workspaces.  This allows us to better utilize an agent's
//  diskspace.

jobMap = Jenkins.instance.itemMap
def maxDaysAge = new Date() - 3
def mac_nodes = []
def win_nodes = []


def mapJob(def dirName, def parent=null){
  //workspace ends with "@tmp" usually maps to a job name w/o "@tmp"
  if(dirName ==~ /.*@tmp$/){
    dirName = dirName -~ /@tmp$/
  }
  def job;
  if(parent != null){
    job = parent.getItem(dirName)
  }else{
    job = jobMap[dirName]
  }
  return job;
}

def deleteOnWinSlave(node, workspace) {

  rootPath=node.getRootPath()
  baseWorkspace = rootPath.child('workspace')

  command="cmd /C cd " + baseWorkspace + " && takeown /F '" +
           workspace + "' /R /D Y /A && rmdir /S /Q '" + workspace + "'"
  launcher = node.createLauncher(listener)
  launcher.decorateFor(node)
  procLauncher = launcher.launch()
  procLauncher = procLauncher.cmdAsSingleString(command)
  //procLauncher.readStdout()
  procLauncher.readStderr()
  proc = procLauncher.start()
  //stdout = proc.getStdout().text
  stderr = proc.getStderr().text
  //println("stdout: ${stdout}")
  println("stdout: ${stderr}")
}

jenkins.model.Jenkins.instance.computers.each { c ->
  if (c.node.nodeName.contains("couchbase-lite-net-validation") && c.node.toComputer().isOnline()) {
    win_nodes.add(c.node)
  }
  if (c.node.nodeName.contains("window") && c.node.toComputer().isOnline()) {
    win_nodes.add(c.node)
  }
  if (c.node.nodeName.contains("mobile-cbl-macosx") && c.node.toComputer().isOnline()) {
    mac_nodes.add(c.node)
  }
}
for (node in mac_nodes) {
  println("Checking workspaces on " + node.nodeName)
  ws = node.getWorkspaceRoot()
  for(dir in ws.listDirectories()){
    if (dir.name ==~ /.*ws-cleanup.*$/){
      println("Removing tmp space of " + dir.name)
      dir.deleteRecursive()
    }
  }
}

for (node in win_nodes) {
  println("Checking workspaces on " + node.nodeName)
  ws = node.getWorkspaceRoot()
  for(dir in ws.listDirectories()){
    def job = mapJob(dir.name)

    if(job != null){
      def jobName = job.getFullDisplayName()

      if (job.isBuilding()) {
        println(".. job " + jobName + " is currently running, skipped")
        continue
       }
    }

    //ws-cleanup workspace is usually left due to permission issues.
    //deleteOnWinSlave will try to retake the ownership before deleting.
    if (dir.name ==~ /.*ws-cleanup.*$/){
      println("Removing tmp space of " + dir.name)
      deleteOnWinSlave(node, dir.name)
      
    }

    //if the workspace wasn't modified recently, delete it.
    def lastModified = new Date(dir.lastModified())
    if (lastModified < maxDaysAge){
        println("${dir.name} was last modified on ${lastModified}.")
        println("Removing " + dir.name)
        try {
           dir.deleteRecursive()
         } catch (IOException) {
            println("Unable to delete ${dir.name}!!!")
            println("Try executing rmdir from ${node.nodeName}.")
            deleteOnWinSlave(node, dir.name)
         }
    } else {
        println("${dir.name} was last modified on ${lastModified}.  It will not be removed")
    }
  }
}
