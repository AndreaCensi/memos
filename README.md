``memos`` --- Advanced memoization function with number or memory size limits
==============================================================================

    memoize_simple => Cache discarded when pickled

    memoize_instance  => Cache is saved when pickled

    momize_limited: like memoize_intance, with additional constraints on number
        of things remembered.

        
    from memos import memoize_limited

    class MyClass():

        @memoize_limited(max_size=max_size, max_mem_MB=max_mem_MB)
        def f1(self, x): 
            return ...
