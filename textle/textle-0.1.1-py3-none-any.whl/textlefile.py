import os
import shutil
from .fileref import FileRef, FileUse, to_fref
import subprocess
from .pipeline import Sink
from watchdog.events import FileSystemEventHandler
from threading import Lock

SEV_ERROR = 1
SEV_INFO  = 2
SEV_DBG   = 3

class Textle(FileSystemEventHandler):
    """
    Wrapper for textle files.

    Various options
    FS Layout:
        layout: flat/bin/segregated, default bin:
            - flat: all files located in root
            - bin: all files located in subdir, pipelines can affect and access other files (good for projects with lots of interconnected pipelines)
            - segregated: all pipelines in subdirs of a subdir, good for projects with lots of conflicting names without need to share resources
        build_dir: path, default .textle
            - where to place the build dir(s) for bin and segregated layouts
        externals: list, default empty
            - list of files to:
                a) copy to the build location
                b) ignore their "tag" (rightmost path segment - extension) if referred to in an INPUT during the copy phase
    
    Build Options:
        parallel: int, default 0
            - number of parallel _pipelines_ to build
    """
    def __init__(self, pipelines, global_options, root_dir):
        self.pipelines = pipelines
        self.global_options = {
            "layout": "bin",
            "build_dir": ".textle",
            "parallel": 0,
            "externals": []
        }

        self.global_options.update(global_options)
        if type(self.global_options["externals"]) is not list:
            self.global_options["externals"] = [self.global_options["externals"]]
        self.root_dir = os.path.abspath(root_dir)
        for j in range(len(self.global_options["externals"])):
            self.global_options["externals"][j] = os.path.join(self.root_dir, self.global_options["externals"][j])

        self.layout_roots()

        # Takes (step info, type, message) and is called during the build process
        self.job_callback = lambda x, y, z: None

        self.build_lock = Lock()

    def with_job_callback(self, cb):
        self.job_callback = cb
        return self

    def layout_roots(self):
        if self.global_options["layout"] == "flat":
            for i in self.pipelines:
                i.root = self.root_dir
        elif self.global_options["layout"] in ["bin", "segregated"]:
            build_dir = os.path.join(self.root_dir, self.global_options["build_dir"])
            for j, i in enumerate(self.pipelines):
                if self.global_options["layout"] == "segregated":
                    i.root = os.path.join(build_dir, "pipe{}".format(j))
                else:
                    i.root = build_dir

    def clean(self):
        if self.global_options["layout"] != "flat":
            shutil.rmtree(os.path.join(self.root_dir, self.global_options["build_dir"]))
        else:
            # todo
            raise NotImplementedError("Not implemented -- todo")

    def get_input_files(self):
        filrefs = set()

        for i in self.pipelines:
            filrefs.union(i.all_inputs)

        return [os.path.join(self.root_dir, x.to_str()) for x in filrefs]

    def build_pipeline(self, pipeline):
        # By design, only the output file and input file(s) are copied.
        # TODO: allow for extra files to be specified in the pipeline global options extra_copy_in and extra_copy_out

        out_file = pipeline.steps[-1].output

        self.job_callback("pipeline", SEV_INFO, "Building {}".format(out_file.to_str()))
        if self.global_options["layout"] != "flat":
            # Copy all inputs
            self.job_callback("copy:in", SEV_DBG, "Copying input")
            for in_ in pipeline.all_inputs:
                self.job_callback("copy:in", SEV_DBG, "Copying input {}".format(in_.to_str()))
                try:
                    if not os.path.exists(os.path.split(os.path.join(pipeline.root, in_.to_str()))[0]):
                        os.makedirs(os.path.split(os.path.join(pipeline.root, in_.to_str()))[0])
                except FileNotFoundError:
                    pass
                # Check if this is an external before copying it
                if not any(os.path.basename(x) == in_.to_str() for x in self.global_options["externals"]):
                    shutil.copy2(os.path.join(self.root_dir, in_.to_str()), os.path.join(pipeline.root, in_.to_str()))
                    
        # Copy externals
        if self.global_options["externals"]:
            self.job_callback("copy:externals", SEV_DBG, "Copying externals")
            for ext in self.global_options["externals"]:
                self.job_callback("copy:externals", SEV_DBG, "Copying external {}".format(ext))
                if not os.path.exists(pipeline.root):
                    os.makedirs(pipeline.root)
                shutil.copy2(ext, os.path.join(pipeline.root, os.path.basename(ext)))

        # Run all steps if they are required, checking before
        did_anything = False
        for step in pipeline.steps:
            if issubclass(step, Sink):
                continue
            if pipeline.step_needs_executing(step):
                did_anything = True
                jobs_required = pipeline.get_jobs(step)
                self.job_callback("step:{}".format(step.name), SEV_DBG, "Got jobs")
                for job in jobs_required:
                    cwd = os.getcwd()
                    try:
                        os.chdir(pipeline.root)
                        self.job_callback("job:{}:{}".format(step.name, job[0]), SEV_DBG, "Command {} starting".format(" ".join(job)))
                        output = subprocess.check_output(job, stderr=subprocess.PIPE, universal_newlines=True)
                        self.job_callback("job:{}:{}".format(step.name, job[0]), SEV_INFO, "Command {} finished sucessfully".format(" ".join(job)))
                    except subprocess.CalledProcessError as e:
                        self.job_callback("job:{}:{}".format(step.name, job[0]), SEV_ERROR, "Command {} exited with code {}.".format(" ".join(job), e.returncode))
                        raise
                    finally:
                        os.chdir(cwd)
                self.job_callback("step:{}".format(step.name), SEV_DBG, "Finished OK")

        if self.global_options["layout"] != "flat":
            # Copy output
            self.job_callback("copy:out", SEV_DBG, "Copying output {}".format(out_file.to_str()))
            shutil.copy(os.path.join(pipeline.root, out_file.to_str()), os.path.join(self.root_dir, out_file.to_str()))

        self.job_callback("pipeline", SEV_INFO, "Built {}".format(out_file.to_str()))

    def build(self, from_file_change=None):
        if from_file_change is not None:
            # Instead of querying all possible pipelines, just check which pipeline this is in and build it
            fref = to_fref(os.path.relpath(from_file_change, self.root_dir), FileUse.INPUT)
            for i in self.pipelines:
                if fref in i.all_inputs:
                    self.build_pipeline(i)
        else:
            for i in self.pipelines:
                self.build_pipeline(i)

    def on_modified(self, event):
        """
        Call build
        """

        if not os.path.isfile(event.src_path):
            return

        with self.build_lock:
            self.build(event.src_path)
