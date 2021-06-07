import hudson.model.*;
import hudson.util.*;
import jenkins.model.*;
import hudson.FilePath.FileCallable;
import hudson.slaves.OfflineCause;
import hudson.node_monitors.*;


jobMaxAge = 5
jobMap = Jenkins.instance.itemMap


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

def nodes = []
jenkins.model.Jenkins.instance.computers.each { c ->
  if (c.node.nodeName.contains("window")) {
    nodes.add(c.node)
  }
}
for (node in nodes) {
  ws = node.getWorkspaceRoot()
  for(dir in ws.listDirectories()){
    //todo: MultiJob or MultiBranch have parent/children jobs
    def job = mapJob(dir.name)

    //remove workspace ended with @tmp regardless of the age
    if (dir.name ==~ /.*@tmp$/){
      println("Removing tmp space of " + dir.name)
      dir.deleteRecursive()
    }

    //delete workspace older than jobMaxAge
    if(job != null){
      def lastBuildAge=(System.currentTimeMillis()-job.getLastBuild().getTimeInMillis()).intdiv(1000).intdiv(3600).intdiv(24)
      if (lastBuildAge > jobMaxAge){
        println("Removing " + dir.name)
        dir.deleteRecursive()
      }
    }
  }
}
