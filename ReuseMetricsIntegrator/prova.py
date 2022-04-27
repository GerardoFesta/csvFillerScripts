import os.path,subprocess
from subprocess import STDOUT,PIPE

PATH="/home/gerardo/VersioniCli/Cli"
JavaPATH="ReuseMetricsComputation.java"
def compile_java(java_file):
    subprocess.check_call(['javac', java_file])

def execute_java(java_file):
    java_class,ext = os.path.splitext(java_file)
    print(java_class)
    cmd = ['java', java_class, PATH]
    proc = subprocess.Popen(cmd, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate(input='SomeInputstring')
    print ('This was "' + stdout + '"')

compile_java(JavaPATH)
execute_java(JavaPATH)
