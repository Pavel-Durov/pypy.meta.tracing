## Regarding my previous problem with jit logs
I was finally able to produce jit logs. My problem was that my test program had a very short loop; when I increased the number of iterations, I got my logs. Here's me on StackOverflow [1]

## SELF-like hashmaps optimisation
I looked at the jit logs before the hashmap optimisation [2]. I could see that some time was spent accessing the hashmap. 
Trace example:
+1807: i113 = call_i(ConstClass(ll_call_lookup_function_trampoline__v48___simple_call__function_ll), p46, p107, i110, 0, descr=<Calli 8 rrii EF=5 OS=4>

Looking at the program [3] logs [4] optimised using SELF-like hashmaps, I can see that it has fewer hashmap access-related traces.

6 traces in 0.0.6 - Not optimised version
3 traces in 0.0.7 - SELF-like maps optimised

However, when running hyperfine benchmarking [5] with my VM program [6] there seems to be a very low impact on program performance.

Questions:
1. Why SELF-like hashmap optimisation is not reflected in benchmark results? Is it something specific to my program (as I had issues with jit logs).
2. In my solution I used purefunction and hint jit annotations, as was demonstrated in the PyPy article [7]. However, I noticed that in Converge example [8]  there was a use of jit.elidable instead of purefunction and also no use of jit hints and- any reasons for that?
3. Is there anything I missed/overlooked in this challenge?

I also found this [9] paper useful to my general understanding.


[1] https://stackoverflow.com/questions/73665618/rpython-jit-logs?noredirect=1#comment130093714_73665618

[2] https://github.com/Pavel-Durov/pypy.meta.tracing/blob/main/log/awk_vm-0.0.6.logfile

[3] https://github.com/Pavel-Durov/pypy.meta.tracing/blob/main/src/awk_vm/program.py#L16

[4] https://github.com/Pavel-Durov/pypy.meta.tracing/blob/main/log/awk_vm-0.0.7.logfile

[5] https://github.com/Pavel-Durov/pypy.meta.tracing/blob/main/log/hyperfine/hashmap-optimisation.logfile

[6] https://github.com/Pavel-Durov/pypy.meta.tracing/blob/main/programs/awk/loops.awk

[7] http://morepypy.blogspot.com/2011/03/controlling-tracing-of-interpreter-with_21.html

[8] https://github.com/ltratt/converge/blob/master/vm/Builtins.py#L100

[9] https://tratt.net/laurie/research/pubs/html/bolz_tratt__the_impact_of_metatracing_on_vm_design_and_implementation/