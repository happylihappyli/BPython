
class _WeakValueDictionary: {

    def __init__(self): {
        self_weakref = _weakref.ref(self)

        # Inlined to avoid issues with inheriting from _weakref.ref before _weakref is
        # set by _setup(). Since there's only one instance of this class, this is
        # not expensive.
        class KeyedRef(_weakref.ref):
            __slots__ = "key",
            def __new__(type, ob, key):
                self = super().__new__(type, ob, type.remove)
                self.key = key
                return self
            def __init__(self, ob, key):
                super().__init__(ob, self.remove)
            @staticmethod
            def remove(wr):
                nonlocal self_weakref
                self = self_weakref()
                if self is not None: {
                    if self._iterating: {
                        self._pending_removals.append(wr.key)
                    }
                    else: {
                        _weakref._remove_dead_weakref(self.data, wr.key)
                    }
                }
        self._KeyedRef = KeyedRef
        self.clear()

        }
    }
