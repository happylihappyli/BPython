
class MockRef:
    pass

class _WeakValueDictionary: {
    def __init__(self): {
        self_weakref = MockRef()
        
        # Some comment
        # Another comment
        class KeyedRef(MockRef):
            __slots__ = "key",
            def __init__(self, ob, key):
                pass
        
        self._KeyedRef = KeyedRef
    }
}

print("Success")
