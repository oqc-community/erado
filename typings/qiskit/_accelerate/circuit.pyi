from _typeshed import Incomplete


class AncillaQubit(Qubit):
    """A qubit used as an ancilla."""

    def __copy__(self, /):
        ...

    def __deepcopy__(self, /, _memo):
        ...

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    _index: Incomplete  # DATA DESCRIPTOR

    _register: Incomplete  # DATA DESCRIPTOR


class AncillaRegister(QuantumRegister):
    """Implement an ancilla register."""

    def __contains__(self, key, /):
        """Return bool(key in self)."""
        ...

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getitem__(self, key, /):
        """Return self[key]."""
        ...

    def __getnewargs__(self, /):
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __len__(self, /):
        """Return len(self)."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        """Helper for pickle."""
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    bit_type: type

    def index(self, /, bit):
        """The index of the given bit in the register."""
        ...

    instances_count: int

    name: Incomplete  # DATA DESCRIPTOR
    """The name of the register."""

    prefix: str

    size: Incomplete  # DATA DESCRIPTOR
    """The size of the register."""

    def __iter__(self):
        """make_stubs: MOCKED TO REGISTER THIS CLASS AS AN OLD-STYLE ITERABLE!"""
        ...


class Annotation:
    """An arbitrary annotation for instructions.

    .. note::

        The annotation framework is a new and evolving component of Qiskit.  We expect the
        functionality of this and its first-class support within the transpiler to expand as we
        get more evidence of how it is used.

    This base class alone has very little prescribed behavior or semantics.  The primary interaction
    is by user- or library subclassing.  See :ref:`circuit-annotation-subclassing` for more detail.

    This is a framework for structuring additional metadata that can be attached to :class:`.BoxOp`
    instructions within a :class:`.QuantumCircuit` and :class:`.DAGCircuit` in ways that can be
    tracked and consumed by arbitrary transpiler passes, including custom passes that are not in
    Qiskit core.

    While the stateful :class:`.PropertySet` used during a compilation also supplies a way for
    custom transpiler passes to store arbitrary "state" objects into the compilation workflow that
    can be retrieved by later compiler passes, the :class:`.PropertySet` is stored next to the
    circuit, and so is most suitable for analyses that relate to the circuit as a whole. An
    :class:`Annotation` is intended to be more local in scope, applying to a box of instructions,
    and further, may still be present in the output of :class:`.transpile`, if it is intended for
    further consumption by a lower-level part of your backend's execution machinery (for example, an
    annotation might include metadata instructing an error-mitigation routine to treat a particular
    box in a special way).

    The :class:`.PassManager` currently does not make any effort to track and validate
    pre-conditions on the validity of an :class:`Annotation`.  That is, if you apply a custom
    annotation to a box of instructions that would be invalidated by certain transformations (such
    as routing, basis-gate decomposition, etc), it is currently up to you as the caller of
    :func:`.transpile` or :func:`.generate_preset_pass_manager` to ensure that the compiler passes
    selected will not invalidate the annotation.  We expect to have more first-class support for
    annotations to declare their validity requirements in the future."""

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        """Helper for pickle."""
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    namespace: str


class Bit:
    """Implement a generic bit.

    .. note::
        This class cannot be instantiated directly. Its only purpose is to allow generic type
        checking for :class:`.Clbit` and :class:`.Qubit`."""

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        """Helper for pickle."""
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...


class BitLocations:
    """"""

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getitem__(self, key, /):
        """Return self[key]."""
        ...

    def __getnewargs__(self, /):
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...


    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __iter__(self, /):
        """Implement iter(self)."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __len__(self, /):
        """Return len(self)."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        """Helper for pickle."""
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    index: Incomplete  # DATA DESCRIPTOR

    registers: Incomplete  # DATA DESCRIPTOR


class CircuitData:
    """A container for :class:`.QuantumCircuit` instruction listings that stores
    :class:`.CircuitInstruction` instances in a packed form by interning
    their :attr:`~.CircuitInstruction.qubits` and
    :attr:`~.CircuitInstruction.clbits` to native vectors of indices.

    Before adding a :class:`.CircuitInstruction` to this container, its
    :class:`.Qubit` and :class:`.Clbit` instances MUST be registered via the
    constructor or via :meth:`.CircuitData.add_qubit` and
    :meth:`.CircuitData.add_clbit`. This is because the order in which
    bits of the same type are added to the container determines their
    associated indices used for storage and retrieval.

    Once constructed, this container behaves like a Python list of
    :class:`.CircuitInstruction` instances. However, these instances are
    created and destroyed on the fly, and thus should be treated as ephemeral.

    For example,

    .. plot::
       :include-source:
       :no-figs:

        qubits = [Qubit()]
        data = CircuitData(qubits)
        data.append(CircuitInstruction(XGate(), (qubits[0],), ()))
        assert(data[0] == data[0]) # => Ok.
        assert(data[0] is data[0]) # => PANICS!

    .. warning::

        This is an internal interface and no part of it should be relied upon
        outside of Qiskit.

    Args:
        qubits (Iterable[:class:`.Qubit`] | None): The initial sequence of
            qubits, used to map :class:`.Qubit` instances to and from its
            indices.
        clbits (Iterable[:class:`.Clbit`] | None): The initial sequence of
            clbits, used to map :class:`.Clbit` instances to and from its
            indices.
        data (Iterable[:class:`.CircuitInstruction`]): An initial instruction
            listing to add to this container. All bits appearing in the
            instructions in this iterable must also exist in ``qubits`` and
            ``clbits``.
        reserve (int): The container's initial capacity. This is reserved
            before copying instructions into the container when ``data``
            is provided, so the initialized container's unused capacity will
            be ``max(0, reserve - len(data))``.

    Raises:
        KeyError: if ``data`` contains a reference to a bit that is not present
            in ``qubits`` or ``clbits``."""

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __delitem__(self, key, /):
        """Delete self[key]."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getitem__(self, key, /):
        """Return self[key]."""
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...


    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __len__(self, /):
        """Return len(self)."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __setitem__(self, key, value, /):
        """Set self[key] to value."""
        ...

    def __setstate__(self, /, state):
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    def _cbit_argument_conversion(self, /, clbit_representation):
        """Converts several clbit representations (such as indexes, range, etc.)
        into a list of qubits.

        Args:
            clbit_representation: Representation to expand.

        Returns:
            The resolved instances of the qubits."""
        ...

    _clbit_indices: Incomplete  # DATA DESCRIPTOR
    """A dict mapping Clbit instances to tuple comprised of 0) the corresponding index in
    circuit.clbits and 1) a list of Register-int pairs for each Register containing the Bit and
    its index within that register."""

    def _qbit_argument_conversion(self, /, qubit_representation):
        """Converts several qubit representations (such as indexes, range, etc.)
        into a list of qubits.

        Args:
            qubit_representation: Representation to expand.

        Returns:
            The resolved instances of the qubits."""
        ...

    _qubit_indices: Incomplete  # DATA DESCRIPTOR
    """A dict mapping Qubit instances to tuple comprised of 0) the corresponding index in
    circuit.qubits and 1) a list of Register-int pairs for each Register containing the Bit and
    its index within that register."""

    def _raw_parameter_table_entry(self, /, param):
        ...

    def active_bits(self, /):
        """Returns a tuple of the sets of :class:`.Qubit` and :class:`.Clbit` instances
        that appear in at least one instruction's bit lists.

        Returns:
            tuple[set[:class:`.Qubit`], set[:class:`.Clbit`]]: The active qubits and clbits."""
        ...

    def add_captured_stretch(self, /, stretch):
        """Add a captured stretch to the circuit.

        Args:
            stretch: the stretch variable to add."""
        ...

    def add_captured_var(self, /, var):
        """Add a captured variable to the circuit.

        Args:
            var: the variable to add."""
        ...

    def add_clbit(self, /, bit, *, strict=True):
        """Registers a :class:`.Clbit` instance.

        Args:
            bit (:class:`.Clbit`): The clbit to register.
            strict (bool): When set, raises an error if ``bit`` is already present.

        Raises:
            ValueError: The specified ``bit`` is already present and flag ``strict``
                was provided."""
        ...

    def add_creg(self, /, register, *, strict=True):
        """Registers a :class:`.QuantumRegister` instance.

        Args:
            bit (:class:`.QuantumRegister`): The register to add."""
        ...

    def add_declared_stretch(self, /, var):
        """Add a local stretch to the circuit.

        Args:
            stretch: the stretch variable to add."""
        ...

    def add_declared_var(self, /, var):
        """Add a local variable to the circuit.

        Args:
            var: the variable to add."""
        ...

    def add_input_var(self, /, var):
        """Add an input variable to the circuit.

        Args:
            var: the variable to add."""
        ...

    def add_qreg(self, /, register, *, strict=True):
        """Registers a :class:`.QuantumRegister` instance.

        Args:
            bit (:class:`.QuantumRegister`): The register to add."""
        ...

    def add_qubit(self, /, bit, *, strict=True):
        """Registers a :class:`.Qubit` instance.

        Args:
            bit (:class:`.Qubit`): The qubit to register.
            strict (bool): When set, raises an error if ``bit`` is already present.

        Raises:
            ValueError: The specified ``bit`` is already present and flag ``strict``
                was provided."""
        ...

    def append(self, /, value):
        """Primary entry point for appending an instruction from Python space."""
        ...

    def append_manual_params(self, /, value, params):
        """Backup entry point for appending an instruction from Python space, in the unusual case that
        one of the instruction parameters contains a cyclical reference to the circuit itself.

        In this case, the `params` field should be a list of `(index, parameters)` tuples, where the
        index is into the instruction's `params` attribute, and `parameters` is a Python iterable
        of `Parameter` objects."""
        ...

    def assign_parameters_iterable(self, /, sequence):
        """Assign all the circuit parameters, given an iterable input of `Param` instances."""
        ...

    def assign_parameters_mapping(self, /, mapping):
        """Assign all uses of the circuit parameters as keys `mapping` to their corresponding values.

        Any items in the mapping that are not present in the circuit are skipped; it's up to Python
        space to turn extra bindings into an error, if they choose to do it."""
        ...

    clbits: Incomplete  # DATA DESCRIPTOR
    """Returns the current sequence of registered :class:`.Clbit`
    instances as a list.

    .. warning::

        Do not modify this list yourself.  It will invalidate the :class:`CircuitData` data
        structures.

    Returns:
        list(:class:`.Clbit`): The current sequence of registered clbits."""

    def clear(self, /):
        ...

    def copy(self, /, copy_instructions=True, deepcopy=False):
        """Performs a shallow copy.

        Returns:
            CircuitData: The shallow copy."""
        ...

    def copy_empty_like(self, /, *, vars_mode=Ellipsis):
        """Performs a copy with no instructions.

        # Arguments:

        * vars_mode: specifies realtime variables copy mode.
            * VarsMode::Alike: variables will be copied following declaration semantics in self.
            * VarsMode::Captures: variables will be copied as captured variables.
            * VarsMode::Drop: variables will not be copied.

        # Returns:

        CircuitData: The empty copy like self."""
        ...

    def count_ops(self, /):
        """Counts the number of times each operation is used in the circuit.

        # Parameters
        - `self` - A mutable reference to the CircuitData struct.

        # Returns
        An IndexMap containing the operation names as keys and their respective counts as values."""
        ...

    cregs: Incomplete  # DATA DESCRIPTOR
    """The list of registered :class:`.ClassicalRegisters` instances.

    .. warning::

        Do not modify this list yourself.  It will invalidate/corrupt :attr:`.data` for this circuit.

    Returns:
        list[:class:`.ClassicalRegister`]: The current sequence of registered qubits."""

    def extend(self, /, itr):
        ...

    def foreach_op(self, /, func):
        """Invokes callable ``func`` with each instruction's operation.

        Args:
            func (Callable[[:class:`~.Operation`], None]):
                The callable to invoke."""
        ...

    def foreach_op_indexed(self, /, func):
        """Invokes callable ``func`` with the positional index and operation
        of each instruction.

        Args:
            func (Callable[[int, :class:`~.Operation`], None]):
                The callable to invoke."""
        ...

    def get_captured_stretches(self, /):
        """Return a list of the captured stretch variables tracked in this circuit."""
        ...

    def get_captured_vars(self, /):
        """Return a list of the captured variables tracked in this circuit."""
        ...

    def get_declared_stretches(self, /):
        """Return a list of the local stretch variables tracked in this circuit."""
        ...

    def get_declared_vars(self, /):
        """Return a list of the local variables tracked in this circuit."""
        ...

    def get_input_vars(self, /):
        """Return a list of the input variables tracked in this circuit"""
        ...

    def get_parameter_by_name(self, /, name):
        ...

    def get_stretch(self, /, name):
        ...

    def get_var(self, /, name):
        ...

    global_phase: Incomplete  # DATA DESCRIPTOR

    def has_captured_stretch(self, /, name):
        """Check if the circuit contains a capture stretch with the given name."""
        ...

    def has_captured_var(self, /, name):
        """Check if the circuit contains a capture variable with the given name."""
        ...

    def has_control_flow_op(self, /):
        """Checks whether the circuit has an instance of :class:`.ControlFlowOp`
        present amongst its operations."""
        ...

    def has_declared_stretch(self, /, name):
        """Check if the circuit contains a local stretch with the given name."""
        ...

    def has_declared_var(self, /, name):
        """Check if the circuit contains a local variable with the given name."""
        ...

    def has_input_var(self, /, name):
        """Check if the circuit contains an input variable with the given name."""
        ...

    def has_stretch(self, /, stretch):
        """Check if this stretch variable is in the circuit.

        Args:
            var: the variable or name to check."""
        ...

    def has_var(self, /, var):
        """Check if this realtime variable is in the circuit.

        Args:
            var: the variable or name to check."""
        ...

    def insert(self, /, index, value):
        ...

    def make_physical(self, /, num_qubits=None):
        """Put ``self`` into the canonical physical form, with the given number of qubits.

        This acts in place, and does not need to traverse the circuit.  It is intended for use when
        the circuit is known to already represent a physical circuit, and we just need to assert
        that it is canonical physical form.

        This erases any information about virtual qubits in the :class:`CircuitData`.  Effectively,
        this applies the "trivial" layout mapping virtual qubit 0 to physical qubit 0, and so on.

        Args:
            num_qubits: if given, the total number of physical qubits in the output; it must be at
                least as large as the number of qubits in the circuit.  If not given, the number of
                qubits is unchanged."""
        ...

    def map_nonstandard_ops(self, /, func):
        """Invokes callable ``func`` with each instruction's operation, replacing the operation with
        the result, if the operation is not a standard gate without a condition.

        .. warning::

            This is a shim for while there are still important components of the circuit still
            implemented in Python space.  This method **skips** any instruction that contains an
            non-conditional standard gate (which is likely to be most instructions).

        Args:
            func (Callable[[:class:`~.Operation`], :class:`~.Operation`]):
                A callable used to map original operations to their replacements."""
        ...

    num_captured_stretches: Incomplete  # DATA DESCRIPTOR
    """Return the number of captured stretch variables in the circuit."""

    num_captured_vars: Incomplete  # DATA DESCRIPTOR
    """Return the number of captured variables in the circuit."""

    num_clbits: Incomplete  # DATA DESCRIPTOR
    """Return the number of clbits. This is equivalent to the length of the list returned by
    :meth:`.CircuitData.clbits`.

    Returns:
        int: The number of clbits."""

    num_declared_stretches: Incomplete  # DATA DESCRIPTOR
    """Return the number of local stretch variables in the circuit."""

    num_declared_vars: Incomplete  # DATA DESCRIPTOR
    """Return the number of local variables in the circuit."""

    num_input_vars: Incomplete  # DATA DESCRIPTOR
    """Return the number of classical input variables in the circuit."""

    def num_nonlocal_gates(self, /):
        ...

    def num_parameters(self, /):
        """Return the number of unbound compile-time symbolic parameters tracked by the circuit."""
        ...

    num_qubits: Incomplete  # DATA DESCRIPTOR
    """Return the number of qubits. This is equivalent to the length of the list returned by
    :meth:`.CircuitData.qubits`

    Returns:
        int: The number of qubits."""

    parameters: Incomplete  # DATA DESCRIPTOR
    """Get a (cached) sorted list of the Python-space `Parameter` instances tracked by this circuit
    data's parameter table."""

    def pop(self, /, index=None):
        ...

    qregs: Incomplete  # DATA DESCRIPTOR
    """The list of registered :class:`.QuantumRegister` instances.

    .. warning::

        Do not modify this list yourself.  It will invalidate/corrupt :attr:`.data` for this circuit.

    Returns:
        list[:class:`.QuantumRegister`]: The current sequence of registered qubits."""

    qubits: Incomplete  # DATA DESCRIPTOR
    """Returns the current sequence of registered :class:`.Qubit` instances as a list.

    .. warning::

        Do not modify this list yourself.  It will invalidate the :class:`CircuitData` data
        structures.

    Returns:
        list(:class:`.Qubit`): The current sequence of registered qubits."""

    def replace_bits(self, /, qubits=None, clbits=None, qregs=None, cregs=None):
        """Replaces the bits of this container with the given ``qubits``
        and/or ``clbits``.

        The `:attr:`~.CircuitInstruction.qubits` and
        :attr:`~.CircuitInstruction.clbits` of existing instructions are
        reinterpreted using the new bit sequences on access.
        As such, the primary use-case for this method is to remap a circuit to
        a different set of bits in constant time relative to the number of
        instructions in the circuit.

        Args:
            qubits (Iterable[:class:`.Qubit] | None):
                The qubit sequence which should replace the container's
                existing qubits, or ``None`` to skip replacement.
            clbits (Iterable[:class:`.Clbit] | None):
                The clbit sequence which should replace the container's
                existing qubits, or ``None`` to skip replacement.

        Raises:
            ValueError: A replacement sequence is smaller than the bit list
                its contents would replace.

        .. note::

            Instruction operations themselves are NOT adjusted.
            To modify bits referenced by an operation, use
            :meth:`~.CircuitData.foreach_op` or
            :meth:`~.CircuitData.foreach_op_indexed` or
            :meth:`~.CircuitData.map_nonstandard_ops` to adjust the operations manually
            after calling this method.

        Examples:

            The following :class:`.CircuitData` is reinterpreted as if its bits
            were originally added in reverse.

            .. code-block::

                qr = QuantumRegister(3)
                data = CircuitData(qubits=qr, data=[
                    CircuitInstruction(XGate(), [qr[0]], []),
                    CircuitInstruction(XGate(), [qr[1]], []),
                    CircuitInstruction(XGate(), [qr[2]], []),
                ])

                data.replace_bits(qubits=reversed(qr))
                assert(data == [
                    CircuitInstruction(XGate(), [qr[2]], []),
                    CircuitInstruction(XGate(), [qr[1]], []),
                    CircuitInstruction(XGate(), [qr[0]], []),
                ])"""
        ...

    def reserve(self, /, additional):
        """Reserves capacity for at least ``additional`` more
        :class:`.CircuitInstruction` instances to be added to this container.

        Args:
            additional (int): The additional capacity to reserve. If the
                capacity is already sufficient, does nothing."""
        ...

    def unsorted_parameters(self, /):
        ...

    def width(self, /):
        """Return the width of the circuit. This is the number of qubits plus the
        number of clbits.

        Returns:
            int: The width of the circuit."""
        ...

    def __iter__(self):
        """make_stubs: MOCKED TO REGISTER THIS CLASS AS AN OLD-STYLE ITERABLE!"""
        ...


class CircuitInstruction:
    """A single instruction in a :class:`.QuantumCircuit`, comprised of the :attr:`operation` and
    various operands.

    .. note::

        There is some possible confusion in the names of this class, :class:`~.circuit.Instruction`,
        and :class:`~.circuit.Operation`, and this class's attribute :attr:`operation`.  Our
        preferred terminology is by analogy to assembly languages, where an "instruction" is made up
        of an "operation" and its "operands".

        Historically, :class:`~.circuit.Instruction` came first, and originally contained the qubits
        it operated on and any parameters, so it was a true "instruction".  Over time,
        :class:`.QuantumCircuit` became responsible for tracking qubits and clbits, and the class
        became better described as an "operation".  Changing the name of such a core object would be
        a very unpleasant API break for users, and so we have stuck with it.

        This class was created to provide a formal "instruction" context object in
        :class:`.QuantumCircuit.data`, which had long been made of ad-hoc tuples.  With this, and
        the advent of the :class:`~.circuit.Operation` interface for adding more complex objects to
        circuits, we took the opportunity to correct the historical naming.  For the time being,
        this leads to an awkward case where :attr:`.CircuitInstruction.operation` is often an
        :class:`~.circuit.Instruction` instance (:class:`~.circuit.Instruction` implements the
        :class:`.Operation` interface), but as the :class:`.Operation` interface gains more use,
        this confusion will hopefully abate.

    .. warning::

        This is a lightweight internal class and there is minimal error checking; you must respect
        the type hints when using it.  It is the user's responsibility to ensure that direct
        mutations of the object do not invalidate the types, nor the restrictions placed on it by
        its context.  Typically this will mean, for example, that :attr:`qubits` must be a sequence
        of distinct items, with no duplicates."""

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getitem__(self, key, /):
        """Return self[key]."""
        ...

    def __getnewargs__(self, /):
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...


    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __iter__(self, /):
        """Implement iter(self)."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __len__(self, /):
        """Return len(self)."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        """Helper for pickle."""
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    def _legacy_format(self, /):
        ...

    clbits: Incomplete  # DATA DESCRIPTOR
    """A sequence of the classical bits that this operation reads from or writes to."""

    def copy(self, /):
        """Returns a shallow copy.

        Returns:
            CircuitInstruction: The shallow copy."""
        ...

    def is_control_flow(self, /):
        """Is the :class:`.Operation` contained in this instruction a control-flow operation (i.e. an
        instance of :class:`.ControlFlowOp`)?"""
        ...

    def is_controlled_gate(self, /):
        """Is the :class:`.Operation` contained in this instruction a subclass of
        :class:`.ControlledGate`?"""
        ...

    def is_directive(self, /):
        """Is the :class:`.Operation` contained in this node a directive?"""
        ...

    def is_parameterized(self, /):
        """Does this instruction contain any :class:`.ParameterExpression` parameters?"""
        ...

    def is_standard_gate(self, /):
        """Is the :class:`.Operation` contained in this instruction a Qiskit standard gate?"""
        ...

    label: Incomplete  # DATA DESCRIPTOR

    matrix: Incomplete  # DATA DESCRIPTOR

    name: Incomplete  # DATA DESCRIPTOR
    """Returns the Instruction name corresponding to the op for this node"""

    operation: Incomplete  # DATA DESCRIPTOR
    """The logical operation that this instruction represents an execution of."""

    params: Incomplete  # DATA DESCRIPTOR

    qubits: Incomplete  # DATA DESCRIPTOR
    """A sequence of the qubits that the operation is applied to."""

    def replace(self, /, operation=None, qubits=None, clbits=None, params=None):
        """Creates a shallow copy with the given fields replaced.

        Returns:
            CircuitInstruction: A new instance with the given fields replaced."""
        ...


class ClassicalRegister(Register):
    """Implement a register."""

    def __contains__(self, key, /):
        """Return bool(key in self)."""
        ...

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getitem__(self, key, /):
        """Return self[key]."""
        ...

    def __getnewargs__(self, /):
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __len__(self, /):
        """Return len(self)."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        """Helper for pickle."""
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    bit_type: type

    def index(self, /, bit):
        """The index of the given bit in the register."""
        ...

    instances_count: int

    name: Incomplete  # DATA DESCRIPTOR
    """The name of the register."""

    prefix: str

    size: Incomplete  # DATA DESCRIPTOR
    """The size of the register."""

    def __iter__(self):
        """make_stubs: MOCKED TO REGISTER THIS CLASS AS AN OLD-STYLE ITERABLE!"""
        ...


class Clbit(Bit):
    """A clbit, which can be compared between different circuits."""

    def __copy__(self, /):
        ...

    def __deepcopy__(self, /, _memo):
        ...

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    _index: Incomplete  # DATA DESCRIPTOR

    _register: Incomplete  # DATA DESCRIPTOR


class DAGCircuit:
    """Quantum circuit as a directed acyclic graph.

    There are 3 types of nodes in the graph: inputs, outputs, and operations.
    The nodes are connected by directed edges that correspond to qubits and
    bits."""

    def __copy__(self, /):
        ...

    def __deepcopy__(self, /, memo):
        ...

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getstate__(self, /):
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...


    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        """Helper for pickle."""
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __setstate__(self, /, state):
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    def _apply_op_node_back(self, /, node, check=False):
        ...

    def _check_condition(self, /, name, condition):
        """Verify that the condition is valid.

        Args:
            name (string): used for error reporting
            condition (tuple or None): a condition tuple (ClassicalRegister, int) or (Clbit, bool)

        Raises:
            DAGCircuitError: if conditioning on an invalid register"""
        ...

    _clbit_indices: Incomplete  # DATA DESCRIPTOR
    """Returns a dict mapping Clbit instances to tuple comprised of 0) the
    corresponding index in circuit.clbits and 1) a list of
    Register-int pairs for each Register containing the Bit and its index
    within that register."""

    _duration: Incomplete  # DATA DESCRIPTOR
    """Returns the total duration of the circuit for internal use (no deprecation warning).

    To be removed with get_duration."""

    def _edges(self, /):
        ...

    def _find_successors_by_edge(self, /, node_index, edge_checker):
        ...

    def _has_edge(self, /, source, target):
        ...

    def _in_edges(self, /, node_index):
        ...

    def _in_wires(self, /, node_index):
        ...

    def _is_dag(self, /):
        ...

    def _out_edges(self, /, node_index):
        ...

    def _out_wires(self, /, node_index):
        ...

    _qubit_indices: Incomplete  # DATA DESCRIPTOR
    """Returns a dict mapping Qubit instances to tuple comprised of 0) the
    corresponding index in circuit.qubits and 1) a list of
    Register-int pairs for each Register containing the Bit and its index
    within that register."""

    def _to_dot(self, /, graph_attrs=None, node_attrs=None, edge_attrs=None):
        ...

    _unit: Incomplete  # DATA DESCRIPTOR
    """Returns the unit that duration is specified in for internal use (no deprecation warning).

    To be removed with get_unit."""

    def add_captured_stretch(self, /, stretch):
        """Add a captured stretch to the circuit.

        Args:
            stretch: the stretch to add."""
        ...

    def add_captured_var(self, /, var):
        """Add a captured variable to the circuit.

        Args:
            var: the variable to add."""
        ...

    def add_clbits(self, /, clbits):
        """Add individual clbit wires."""
        ...

    def add_creg(self, /, creg):
        """Add all wires in a classical register."""
        ...

    def add_declared_stretch(self, /, stretch):
        """Add a declared stretch to the circuit.

        Args:
            stretch: the stretch to add."""
        ...

    def add_declared_var(self, /, var):
        """Add a declared local variable to the circuit.

        Args:
            var: the variable to add."""
        ...

    def add_input_var(self, /, var):
        """Add an input variable to the circuit.

        Args:
            var: the variable to add."""
        ...

    def add_qreg(self, /, qreg):
        """Add all wires in a quantum register."""
        ...

    def add_qubits(self, /, qubits):
        """Add individual qubit wires."""
        ...

    def ancestors(self, /, node):
        """Returns set of the ancestors of a node as :class:`.DAGOpNode` s and :class:`.DAGInNode` s.

        The ancestors are the set of all nodes that can reach the target node. Whereas the
        :meth:`.DAGCircuit.predecessors` only contains the immediate predecessors, the ancestors
        recursively contain the predecessors of each predecessor."""
        ...

    def apply_operation_back(self, /, op, qargs=None, cargs=None, *, check=True):
        """Apply an operation to the output of the circuit.

        Args:
            op (qiskit.circuit.Operation): the operation associated with the DAG node
            qargs (tuple[~qiskit.circuit.Qubit]): qubits that op will be applied to
            cargs (tuple[Clbit]): cbits that op will be applied to
            check (bool): If ``True`` (default), this function will enforce that the
                :class:`.DAGCircuit` data-structure invariants are maintained (all ``qargs`` are
                :class:`~.circuit.Qubit` s, all are in the DAG, etc).  If ``False``, the caller *must*
                uphold these invariants itself, but the cost of several checks will be skipped.
                This is most useful when building a new DAG from a source of known-good nodes.
        Returns:
            DAGOpNode: the node for the op that was added to the dag

        Raises:
            DAGCircuitError: if a leaf node is connected to multiple outputs"""
        ...

    def apply_operation_front(self, /, op, qargs=None, cargs=None, *, check=True):
        """Apply an operation to the input of the circuit.

        Args:
            op (qiskit.circuit.Operation): the operation associated with the DAG node
            qargs (tuple[~qiskit.circuit.Qubit]): qubits that op will be applied to
            cargs (tuple[Clbit]): cbits that op will be applied to
            check (bool): If ``True`` (default), this function will enforce that the
                :class:`.DAGCircuit` data-structure invariants are maintained (all ``qargs`` are
                :class:`~.circuit.Qubit` s, all are in the DAG, etc).  If ``False``, the caller *must*
                uphold these invariants itself, but the cost of several checks will be skipped.
                This is most useful when building a new DAG from a source of known-good nodes.
        Returns:
            DAGOpNode: the node for the op that was added to the dag

        Raises:
            DAGCircuitError: if initial nodes connected to multiple out edges"""
        ...

    def bfs_successors(self, /, node):
        """Returns an iterator of tuples of ``(DAGNode, [DAGNodes])`` where the ``DAGNode`` is the
        current node and ``[DAGNodes]`` is a list of the successors in BFS order."""
        ...

    def classical_predecessors(self, /, node):
        """Returns iterator of the predecessors of a node that are
        connected by a classical edge as DAGOpNodes and DAGInNodes."""
        ...

    def classical_successors(self, /, node):
        """Returns iterator of the successors of a node that are
        connected by a classical edge as DAGOpNodes and DAGOutNodes."""
        ...

    clbits: Incomplete  # DATA DESCRIPTOR
    """Returns the current sequence of registered :class:`.Clbit`
    instances as a list.

    .. warning::

        Do not modify this list yourself.  It will invalidate the :class:`DAGCircuit` data
        structures.

    Returns:
        list(:class:`.Clbit`): The current sequence of registered clbits."""

    def collect_1q_runs(self, /):
        """Return a set of non-conditional runs of 1q "op" nodes."""
        ...

    def collect_2q_runs(self, /):
        """Return a set of non-conditional runs of 2q "op" nodes."""
        ...

    def collect_runs(self, /, namelist):
        """Return a set of non-conditional runs of "op" nodes with the given names.

        For example, "... h q[0]; cx q[0],q[1]; cx q[0],q[1]; h q[1]; .."
        would produce the tuple of cx nodes as an element of the set returned
        from a call to collect_runs(["cx"]). If instead the cx nodes were
        "cx q[0],q[1]; cx q[1],q[0];", the method would still return the
        pair in a tuple. The namelist can contain names that are not
        in the circuit's basis.

        Nodes must have only one successor to continue the run."""
        ...

    def compose(self, /, other, qubits=None, clbits=None, front=False, inplace=True, *, inline_captures=False):
        """Compose the ``other`` circuit onto the output of this circuit.

        A subset of input wires of ``other`` are mapped
        to a subset of output wires of this circuit.

        ``other`` can be narrower or of equal width to ``self``.

        Args:
            other (DAGCircuit): circuit to compose with self
            qubits (list[~qiskit.circuit.Qubit|int]): qubits of self to compose onto.
            clbits (list[Clbit|int]): clbits of self to compose onto.
            front (bool): If True, front composition will be performed (not implemented yet)
            inplace (bool): If True, modify the object. Otherwise return composed circuit.
            inline_captures (bool): If ``True``, variables marked as "captures" in the ``other`` DAG
                will be inlined onto existing uses of those same variables in ``self``.  If ``False``,
                all variables in ``other`` are required to be distinct from ``self``, and they will
                be added to ``self``.

        ..
            Note: unlike `QuantumCircuit.compose`, there's no `var_remap` argument here.  That's
            because the `DAGCircuit` inner-block structure isn't set up well to allow the recursion,
            and `DAGCircuit.compose` is generally only used to rebuild a DAG from layers within
            itself than to join unrelated circuits.  While there's no strong motivating use-case
            (unlike the `QuantumCircuit` equivalent), it's safer and more performant to not provide
            the option.

        Returns:
           DAGCircuit: the composed dag (returns None if inplace==True).

        Raises:
            DAGCircuitError: if ``other`` is wider or there are duplicate edge mappings."""
        ...

    def control_flow_op_nodes(self, /):
        """Get a list of "op" nodes in the dag that contain control flow instructions.

        Returns:
            list[DAGOpNode]: The list of dag nodes containing control flow ops."""
        ...

    def copy_empty_like(self, /, *, vars_mode=Ellipsis):
        """Return a copy of self with the same structure but empty.

        That structure includes:
            * name and other metadata
            * global phase
            * duration
            * all the qubits and clbits, including the registers.

        Returns:
            DAGCircuit: An empty copy of self."""
        ...

    def count_ops(self, /, *, recurse=True):
        """Count the occurrences of operation names.

        Args:
            recurse: if ``True`` (default), then recurse into control-flow operations.  In all
                cases, this counts only the number of times the operation appears in any possible
                block; both branches of if-elses are counted, and for- and while-loop blocks are
                only counted once.

        Returns:
            Mapping[str, int]: a mapping of operation names to the number of times it appears."""
        ...

    def count_ops_longest_path(self, /):
        """Count the occurrences of operation names on the longest path.

        Returns a dictionary of counts keyed on the operation name."""
        ...

    cregs: Incomplete  # DATA DESCRIPTOR
    """Returns the dict containing the ClassicalRegisters in the circuit"""

    def depth(self, /, *, recurse=False):
        """Return the circuit depth.  If there is control flow present, this count may only be an
        estimate, as the complete control-flow path cannot be statically known.

        Args:
            recurse: if ``True``, then recurse into control-flow operations.  For loops
                with known-length iterators are counted as if the loop had been manually unrolled
                (*i.e.* with each iteration of the loop body written out explicitly).
                If-else blocks take the longer case of the two branches.  While loops are counted as
                if the loop body runs once only.  Defaults to ``False`` and raises
                :class:`.DAGCircuitError` if any control flow is present, to avoid silently
                returning a nonsensical number.

        Returns:
            int: the circuit depth

        Raises:
            DAGCircuitError: if not a directed acyclic graph
            DAGCircuitError: if unknown control flow is present in a recursive call, or any control
                flow is present in a non-recursive call."""
        ...

    def descendants(self, /, node):
        """Returns set of the descendants of a node as :class:`.DAGOpNode` s and :class:`.DAGOutNode` s.

        The descendants are the set of all nodes that can be reached from the target node. In
        comparison, :meth:`.DAGCircuit.successors` is an iterator over the immediate successors,
        whereas this method contains all the successors' succesors."""
        ...

    def draw(self, /, scale=0.7, filename=None, style='color'):
        """Draws the dag circuit.

        This function needs `Graphviz <https://www.graphviz.org/>`_ to be
        installed. Graphviz is not a python package and can't be pip installed
        (the ``graphviz`` package on PyPI is a Python interface library for
        Graphviz and does not actually install Graphviz). You can refer to
        `the Graphviz documentation <https://www.graphviz.org/download/>`__ on
        how to install it.

        Args:
            scale (float): scaling factor
            filename (str): file path to save image to (format inferred from name)
            style (str):
                'plain': B&W graph;
                'color' (default): color input/output/op nodes

        Returns:
            Ipython.display.Image: if in Jupyter notebook and not saving to file,
            otherwise None."""
        ...

    duration: Incomplete  # DATA DESCRIPTOR
    """Returns the total duration of the circuit, set by a scheduling transpiler pass. Its unit is
    specified by :attr:`.unit`

    DEPRECATED since Qiskit 1.3.0 and will be removed in Qiskit 3.0.0"""

    def edges(self, /, nodes=None):
        """Iterator for edge values with source and destination node.

        This works by returning the outgoing edges from the specified nodes. If
        no nodes are specified all edges from the graph are returned.

        Args:
            nodes(DAGOpNode, DAGInNode, or DAGOutNode|list(DAGOpNode, DAGInNode, or DAGOutNode):
                Either a list of nodes or a single input node. If none is specified,
                all edges are returned from the graph.

        Yield:
            edge: the edge as a tuple with the format
                (source node, destination node, edge wire)"""
        ...

    def find_bit(self, /, bit):
        """Finds locations in the circuit, by mapping the Qubit and Clbit to positional index
        BitLocations is defined as: BitLocations = namedtuple("BitLocations", ("index", "registers"))

        Args:
            bit (Bit): The bit to locate.

        Returns:
            namedtuple(int, List[Tuple(Register, int)]): A 2-tuple. The first element (``index``)
                contains the index at which the ``Bit`` can be found (in either
                :obj:`~DAGCircuit.qubits`, :obj:`~DAGCircuit.clbits`, depending on its
                type). The second element (``registers``) is a list of ``(register, index)``
                pairs with an entry for each :obj:`~Register` in the circuit which contains the
                :obj:`~Bit` (and the index in the :obj:`~Register` at which it can be found).

          Raises:
            DAGCircuitError: If the supplied :obj:`~Bit` was of an unknown type.
            DAGCircuitError: If the supplied :obj:`~Bit` could not be found on the circuit."""
        ...

    def front_layer(self, /):
        """Return a list of op nodes in the first layer of this dag."""
        ...

    def gate_nodes(self, /):
        """Get the list of gate nodes in the dag.

        Returns:
            list[DAGOpNode]: the list of DAGOpNodes that represent gates."""
        ...

    global_phase: Incomplete  # DATA DESCRIPTOR
    """Return the global phase of the circuit."""

    def has_identifier(self, /, var):
        """Is this identifier in the DAG?

        Args:
            var: the identifier or name to check."""
        ...

    def has_stretch(self, /, var):
        """Is this stretch in the DAG?

        Args:
            var: the stretch or name to check."""
        ...

    def has_var(self, /, var):
        """Is this realtime variable in the DAG?

        Args:
            var: the variable or name to check."""
        ...

    def idle_wires(self, /, ignore=None):
        """Return idle wires.

        Args:
            ignore (list(str)): List of node names to ignore. Default: []

        Yields:
            Bit: Bit in idle wire.

        Raises:
            DAGCircuitError: If the DAG is invalid"""
        ...

    input_map: Incomplete  # DATA DESCRIPTOR

    def is_predecessor(self, /, node, node_pred):
        """Checks if a second node is in the predecessors of node."""
        ...

    def is_successor(self, /, node, node_succ):
        """Checks if a second node is in the successors of node."""
        ...

    def iter_captured_stretches(self, /):
        """Iterable over the captured stretches tracked by the circuit."""
        ...

    def iter_captured_vars(self, /):
        """Iterable over the captured classical variables tracked by the circuit."""
        ...

    def iter_captures(self, /):
        """Iterable over all captured identifiers tracked by the circuit."""
        ...

    def iter_declared_stretches(self, /):
        """Iterable over the declared stretches tracked by the circuit."""
        ...

    def iter_declared_vars(self, /):
        """Iterable over the declared classical variables tracked by the circuit."""
        ...

    def iter_input_vars(self, /):
        """Iterable over the input classical variables tracked by the circuit."""
        ...

    def iter_stretches(self, /):
        """Iterable over all the stretches tracked by the circuit."""
        ...

    def iter_vars(self, /):
        """Iterable over all the classical variables tracked by the circuit."""
        ...

    def layers(self, /, *, vars_mode=Ellipsis):
        """Yield a shallow view on a layer of this DAGCircuit for all d layers of this circuit.

        A layer is a circuit whose gates act on disjoint qubits, i.e.,
        a layer has depth 1. The total number of layers equals the
        circuit depth d. The layers are indexed from 0 to d-1 with the
        earliest layer at index 0. The layers are constructed using a
        greedy algorithm. Each returned layer is a dict containing
        {"graph": circuit graph, "partition": list of qubit lists}.

        The returned layer contains new (but semantically equivalent) DAGOpNodes, DAGInNodes,
        and DAGOutNodes. These are not the same as nodes of the original dag, but are equivalent
        via DAGNode.semantic_eq(node1, node2).

        TODO: Gates that use the same cbits will end up in different
        layers as this is currently implemented. This may not be
        the desired behavior."""
        ...

    def longest_path(self, /):
        """Returns the longest path in the dag as a list of DAGOpNodes, DAGInNodes, and DAGOutNodes."""
        ...

    def make_physical(self, /, num_qubits=None):
        """Put ``self`` into the canonical physical form, with the given number of qubits.

        This acts in place, and does not need to traverse the DAG.  It is intended for use when the
        DAG is known to already represent a physical circuit, and we just need to assert that it is
        canonical physical form.

        This erases any information about virtual qubits in the :class:`DAGCircuit`; if using this
        yourself, you may need to ensure you have created and stored a suitable :class:`.Layout`.
        Effectively, this applies the "trivial" layout mapping virtual qubit 0 to physical qubit 0,
        and so on.

        Args:
            num_qubits: if given, the total number of physical qubits in the output; it must be at
                least as large as the number of qubits in the DAG.  If not given, the number of
                qubits is unchanged."""
        ...

    metadata: Incomplete  # DATA DESCRIPTOR
    """Circuit metadata"""

    def multi_qubit_ops(self, /):
        """Get list of 3+ qubit operations. Ignore directives like snapshot and barrier."""
        ...

    def multigraph_layers(self, /):
        """Yield layers of the multigraph."""
        ...

    name: Incomplete  # DATA DESCRIPTOR
    """Circuit name.  Generally, this corresponds to the name
    of the QuantumCircuit from which the DAG was generated."""

    def named_nodes(self, /, *names):
        """Get the set of "op" nodes with the given name."""
        ...

    def node(self, /, node_id):
        """Get the node in the dag.

        Args:
            node_id(int): Node identifier.

        Returns:
            node: the node."""
        ...

    node_counter: Incomplete  # DATA DESCRIPTOR
    """Returns the number of nodes in the dag."""

    def nodes(self, /):
        """Iterator for node values.

        Yield:
            node: the node."""
        ...

    def nodes_on_wire(self, /, wire, only_ops=False):
        """Iterator for nodes that affect a given wire.

        Args:
            wire (Bit): the wire to be looked at.
            only_ops (bool): True if only the ops nodes are wanted;
                        otherwise, all nodes are returned.
        Yield:
             Iterator: the successive nodes on the given wire

        Raises:
            DAGCircuitError: if the given wire doesn't exist in the DAG"""
        ...

    num_captured_stretches: Incomplete  # DATA DESCRIPTOR
    """Number of captured stretches tracked by the circuit."""

    num_captured_vars: Incomplete  # DATA DESCRIPTOR
    """Number of captured classical variables tracked by the circuit."""

    def num_clbits(self, /):
        """Return the total number of classical bits used by the circuit."""
        ...

    num_declared_stretches: Incomplete  # DATA DESCRIPTOR
    """Number of declared local stretches tracked by the circuit."""

    num_declared_vars: Incomplete  # DATA DESCRIPTOR
    """Number of declared local classical variables tracked by the circuit."""

    num_input_vars: Incomplete  # DATA DESCRIPTOR
    """Number of input classical variables tracked by the circuit."""

    def num_ops(self, /):
        """Get the number of op nodes in the DAG."""
        ...

    def num_qubits(self, /):
        """Return the total number of qubits used by the circuit.
        num_qubits() replaces former use of width().
        DAGCircuit.width() now returns qubits + clbits for
        consistency with Circuit.width() [qiskit-terra #2564]."""
        ...

    num_stretches: Incomplete  # DATA DESCRIPTOR
    """Total number of stretches tracked by the circuit."""

    def num_tensor_factors(self, /):
        """Compute how many components the circuit can decompose into."""
        ...

    num_vars: Incomplete  # DATA DESCRIPTOR
    """Total number of classical variables tracked by the circuit."""

    def op_nodes(self, /, op=None, include_directives=True):
        """Get the list of "op" nodes in the dag.

        Args:
            op (Type): :class:`qiskit.circuit.Operation` subclass op nodes to
                return. If None, return all op nodes.
            include_directives (bool): include `barrier`, `snapshot` etc.

        Returns:
            list[DAGOpNode]: the list of dag nodes containing the given op."""
        ...

    def op_predecessors(self, /, node):
        """Returns the iterator of "op" predecessors of a node in the dag."""
        ...

    def op_successors(self, /, node):
        """Returns iterator of "op" successors of a node in the dag."""
        ...

    output_map: Incomplete  # DATA DESCRIPTOR

    def predecessors(self, /, node):
        """Returns iterator of the predecessors of a node as :class:`.DAGOpNode` s and
        :class:`.DAGInNode` s."""
        ...

    def properties(self, /):
        """Return a dictionary of circuit properties."""
        ...

    qregs: Incomplete  # DATA DESCRIPTOR
    """Returns the dict containing the QuantumRegisters in the circuit"""

    def quantum_causal_cone(self, /, qubit):
        """Returns causal cone of a qubit.

        A qubit's causal cone is the set of qubits that can influence the output of that
        qubit through interactions, whether through multi-qubit gates or operations. Knowing
        the causal cone of a qubit can be useful when debugging faulty circuits, as it can
        help identify which wire(s) may be causing the problem.

        This method does not consider any classical data dependency in the ``DAGCircuit``,
        classical bit wires are ignored for the purposes of building the causal cone.

        Args:
            qubit (~qiskit.circuit.Qubit): The output qubit for which we want to find the causal cone.

        Returns:
            Set[~qiskit.circuit.Qubit]: The set of qubits whose interactions affect ``qubit``."""
        ...

    def quantum_predecessors(self, /, node):
        """Returns iterator of the predecessors of a node that are
        connected by a quantum edge as DAGOpNodes and DAGInNodes."""
        ...

    def quantum_successors(self, /, node):
        """Returns iterator of the successors of a node that are
        connected by a quantum edge as DAGOpNodes and DAGOutNodes."""
        ...

    qubits: Incomplete  # DATA DESCRIPTOR
    """Returns the current sequence of registered :class:`.Qubit` instances as a list.

    .. warning::

        Do not modify this list yourself.  It will invalidate the :class:`DAGCircuit` data
        structures.

    Returns:
        list(:class:`.Qubit`): The current sequence of registered qubits."""

    def remove_all_ops_named(self, /, opname):
        """Remove all operation nodes with the given name."""
        ...

    def remove_ancestors_of(self, /, node):
        """Remove all of the ancestor operation nodes of node."""
        ...

    def remove_clbits(self, /, *clbits):
        """Remove classical bits from the circuit. All bits MUST be idle.
        Any registers with references to at least one of the specified bits will
        also be removed.

        .. warning::
            This method is rather slow, since it must iterate over the entire
            DAG to fix-up bit indices.

        Args:
            clbits (List[Clbit]): The bits to remove.

        Raises:
            DAGCircuitError: a clbit is not a :obj:`.Clbit`, is not in the circuit,
                or is not idle."""
        ...

    def remove_cregs(self, /, *cregs):
        """Remove classical registers from the circuit, leaving underlying bits
        in place.

        Raises:
            DAGCircuitError: a creg is not a ClassicalRegister, or is not in
            the circuit."""
        ...

    def remove_descendants_of(self, /, node):
        """Remove all of the descendant operation nodes of node."""
        ...

    def remove_nonancestors_of(self, /, node):
        """Remove all of the non-ancestors operation nodes of node."""
        ...

    def remove_nondescendants_of(self, /, node):
        """Remove all of the non-descendants operation nodes of node."""
        ...

    def remove_op_node(self, /, node):
        """Remove an operation node n.

        Add edges from predecessors to successors."""
        ...

    def remove_qregs(self, /, *qregs):
        """Remove quantum registers from the circuit, leaving underlying bits
        in place.

        Raises:
            DAGCircuitError: a qreg is not a QuantumRegister, or is not in
            the circuit."""
        ...

    def remove_qubits(self, /, *qubits):
        """Remove quantum bits from the circuit. All bits MUST be idle.
        Any registers with references to at least one of the specified bits will
        also be removed.

        .. warning::
            This method is rather slow, since it must iterate over the entire
            DAG to fix-up bit indices.

        Args:
            qubits (List[~qiskit.circuit.Qubit]): The bits to remove.

        Raises:
            DAGCircuitError: a qubit is not a :obj:`~.circuit.Qubit`, is not in the circuit,
                or is not idle."""
        ...

    def replace_block_with_op(self, /, node_block, op, wire_pos_map, cycle_check=True):
        """Replace a block of nodes with a single node.

        This is used to consolidate a block of DAGOpNodes into a single
        operation. A typical example is a block of gates being consolidated
        into a single ``UnitaryGate`` representing the unitary matrix of the
        block.

        Args:
            node_block (List[DAGNode]): A list of dag nodes that represents the
                node block to be replaced
            op (qiskit.circuit.Operation): The operation to replace the
                block with
            wire_pos_map (Dict[Bit, int]): The dictionary mapping the bits to their positions in the
                output ``qargs`` or ``cargs``. This is necessary to reconstruct the arg order over
                multiple gates in the combined single op node.  If a :class:`.Bit` is not in the
                dictionary, it will not be added to the args; this can be useful when dealing with
                control-flow operations that have inherent bits in their ``condition`` or ``target``
                fields.
            cycle_check (bool): When set to True this method will check that
                replacing the provided ``node_block`` with a single node
                would introduce a cycle (which would invalidate the
                ``DAGCircuit``) and will raise a ``DAGCircuitError`` if a cycle
                would be introduced. This checking comes with a run time
                penalty. If you can guarantee that your input ``node_block`` is
                a contiguous block and won't introduce a cycle when it's
                contracted to a single node, this can be set to ``False`` to
                improve the runtime performance of this method.

        Raises:
            DAGCircuitError: if ``cycle_check`` is set to ``True`` and replacing
                the specified block introduces a cycle or if ``node_block`` is
                empty.

        Returns:
            DAGOpNode: The op node that replaces the block."""
        ...

    def reverse_ops(self, /):
        """Reverse the operations in the ``self`` circuit.

        Returns:
            DAGCircuit: the reversed dag."""
        ...

    def separable_circuits(self, /, remove_idle_qubits=False, *, vars_mode=Ellipsis):
        """Decompose the circuit into sets of qubits with no gates connecting them.

        Args:
            remove_idle_qubits (bool): Flag denoting whether to remove idle qubits from
                the separated circuits. If ``False``, each output circuit will contain the
                same number of qubits as ``self``.

        Returns:
            List[DAGCircuit]: The circuits resulting from separating ``self`` into sets
                of disconnected qubits

        Each :class:`~.DAGCircuit` instance returned by this method will contain the same number of
        clbits as ``self``. The global phase information in ``self`` will not be maintained
        in the subcircuits returned by this method."""
        ...

    def serial_layers(self, /, *, vars_mode=Ellipsis):
        """Yield a layer for all gates of this circuit.

        A serial layer is a circuit with one gate. The layers have the
        same structure as in layers()."""
        ...

    def size(self, /, *, recurse=False):
        """Return the number of operations.  If there is control flow present, this count may only
        be an estimate, as the complete control-flow path cannot be statically known.

        Args:
            recurse: if ``True``, then recurse into control-flow operations.  For loops with
                known-length iterators are counted unrolled.  If-else blocks sum both of the two
                branches.  While loops are counted as if the loop body runs once only.  Defaults to
                ``False`` and raises :class:`.DAGCircuitError` if any control flow is present, to
                avoid silently returning a mostly meaningless number.

        Returns:
            int: the circuit size

        Raises:
            DAGCircuitError: if an unknown :class:`.ControlFlowOp` is present in a call with
                ``recurse=True``, or any control flow is present in a non-recursive call."""
        ...

    def structurally_equal(self, /, other):
        """Are these two DAGs structurally equal?

        This function returns true iff the graph structures are precisely the same as each other,
        including the valid node indices, edge orders, and so on.  This is a much stricter check
        than graph equivalence, and is mostly useful for testing if two :class:`DAGCircuit`
        instances have been constructed and manipulated in the exact same ways.  For example, this
        method can be used to test whether a sequence of manipulations of a DAG is deterministic.

        This method does not consider tracking metadata such as :attr:`metadata` or :attr:`name`,
        but does consider many low-level implementation details of the internal representation, many
        of which do not change the semantics of the circuit.

        This method should, in general, be much faster than graph-equivalence checks, but will
        return ``False`` in many more situations.  This method should never return ``True`` when a
        graph-equivalence check would return ``False``.

        .. note::

            This currently does not handle control flow, because of technical limitations in the
            internal representation of control flow, and will return `false` if any control-flow
            operation is present, even if they are individually equal.

        .. seealso::
            The ``==`` operator
                :class:`DAGCircuit` implements :func:`~object.__eq__` between itself and other
                :class:`DAGCircuit` instances (this same method also powers
                :class:`.QuantumCircuit`'s equality check).  This implements a semantic
                data-flow equality check, which is less sensitive to the order operations were
                defined.  This is typically what a user cares about with respect to equality."""
        ...

    def substitute_node(self, /, node, op, inplace=False, propagate_condition=None):
        """Replace a DAGOpNode with a single operation. qargs, cargs and
        conditions for the new operation will be inferred from the node to be
        replaced. The new operation will be checked to match the shape of the
        replaced operation.

        Args:
            node (DAGOpNode): Node to be replaced
            op (qiskit.circuit.Operation): The :class:`qiskit.circuit.Operation`
                instance to be added to the DAG
            inplace (bool): Optional, default False. If True, existing DAG node
                will be modified to include op. Otherwise, a new DAG node will
                be used.
            propagate_condition (bool): DEPRECATED a legacy option that used
                to control the behavior of handling control flow. It has no
                effect anymore, left it for backwards compatibility. Will be
                removed in Qiskit 3.0.


        Returns:
            DAGOpNode: the new node containing the added operation.

        Raises:
            DAGCircuitError: If replacement operation was incompatible with
            location of target node."""
        ...

    def substitute_node_with_dag(self, /, node, input_dag, wires=None, propagate_condition=None):
        """Replace one node with dag.

        Args:
            node (DAGOpNode): node to substitute
            input_dag (DAGCircuit): circuit that will substitute the node
            wires (list[Bit] | Dict[Bit, Bit]): gives an order for (qu)bits
                in the input circuit. If a list, then the bits refer to those in the ``input_dag``,
                and the order gets matched to the node wires by qargs first, then cargs, then
                conditions.  If a dictionary, then a mapping of bits in the ``input_dag`` to those
                that the ``node`` acts on.
            propagate_condition (bool): DEPRECATED a legacy option that used
                to control the behavior of handling control flow. It has no
                effect anymore, left it for backwards compatibility. Will be
                removed in Qiskit 3.0.

        Returns:
            dict: maps node IDs from `input_dag` to their new node incarnations in `self`.

        Raises:
            DAGCircuitError: if met with unexpected predecessor/successors"""
        ...

    def successors(self, /, node):
        """Returns iterator of the successors of a node as :class:`.DAGOpNode` s and
        :class:`.DAGOutNode` s."""
        ...

    def swap_nodes(self, /, node1, node2):
        """Swap connected nodes e.g. due to commutation.

        Args:
            node1 (OpNode): predecessor node
            node2 (OpNode): successor node

        Raises:
            DAGCircuitError: if either node is not an OpNode or nodes are not connected"""
        ...

    def topological_nodes(self, /, key=None):
        """Yield nodes in topological order.

        Args:
            key (Callable): A callable which will take a DAGNode object and
                return a string sort key. If not specified the bit qargs and
                cargs of a node will be used for sorting.

        Returns:
            generator(DAGOpNode, DAGInNode, or DAGOutNode): node in topological order"""
        ...

    def topological_op_nodes(self, /, key=None):
        """Yield op nodes in topological order.

        Allowed to pass in specific key to break ties in top order

        Args:
            key (Callable): A callable which will take a DAGNode object and
                return a string sort key. If not specified the qargs and
                cargs of a node will be used for sorting.

        Returns:
            generator(DAGOpNode): op node in topological order"""
        ...

    def two_qubit_ops(self, /):
        """Get list of 2 qubit operations. Ignore directives like snapshot and barrier."""
        ...

    unit: Incomplete  # DATA DESCRIPTOR
    """Returns the unit that duration is specified in.

    DEPRECATED since Qiskit 1.3.0 and will be removed in Qiskit 3.0.0"""

    def width(self, /):
        """Return the total number of qubits + clbits used by the circuit.
        This function formerly returned the number of qubits by the calculation
        return len(self._wires) - self.num_clbits()
        but was changed by issue #2564 to return number of qubits + clbits
        with the new function DAGCircuit.num_qubits replacing the former
        semantic of DAGCircuit.width()."""
        ...

    wires: Incomplete  # DATA DESCRIPTOR
    """Return a list of the wires in order."""


class DAGInNode(DAGNode):
    """Object to represent an incoming wire node in the DAGCircuit."""

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getstate__(self, /):
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __setstate__(self, /, state):
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    _node_id: Incomplete  # DATA DESCRIPTOR

    wire: Incomplete  # DATA DESCRIPTOR


class DAGNode:
    """Parent class for DAGOpNode, DAGInNode, and DAGOutNode."""

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getstate__(self, /):
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        """Helper for pickle."""
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __setstate__(self, /, index=None):
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    _node_id: Incomplete  # DATA DESCRIPTOR


class DAGOpNode(DAGNode):
    """Object to represent an Instruction at a node in the DAGCircuit."""

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getstate__(self, /):
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __setstate__(self, /, state):
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    _node_id: Incomplete  # DATA DESCRIPTOR

    def _to_circuit_instruction(self, /, *, deepcopy=False):
        """Get a `CircuitInstruction` that represents the same information as this `DAGOpNode`.  If
        `deepcopy`, any internal Python objects are deep-copied.

        Note: this ought to be a temporary method, while the DAG/QuantumCircuit converters still go
        via Python space; this still involves copy-out and copy-in of the data, whereas doing it all
        within Rust space could directly re-pack the instruction from a `DAGOpNode` to a
        `PackedInstruction` with no intermediate copy."""
        ...

    cargs: Incomplete  # DATA DESCRIPTOR

    definition: Incomplete  # DATA DESCRIPTOR

    def is_control_flow(self, /):
        """Is the :class:`.Operation` contained in this node a control-flow operation (i.e. an instance
        of :class:`.ControlFlowOp`)?"""
        ...

    def is_controlled_gate(self, /):
        """Is the :class:`.Operation` contained in this node a subclass of :class:`.ControlledGate`?"""
        ...

    def is_directive(self, /):
        """Is the :class:`.Operation` contained in this node a directive?"""
        ...

    def is_parameterized(self, /):
        """Does this node contain any :class:`.ParameterExpression` parameters?"""
        ...

    def is_standard_gate(self, /):
        """Is the :class:`.Operation` contained in this node a Qiskit standard gate?"""
        ...

    label: Incomplete  # DATA DESCRIPTOR

    matrix: Incomplete  # DATA DESCRIPTOR

    name: Incomplete  # DATA DESCRIPTOR
    """Returns the Instruction name corresponding to the op for this node"""

    num_clbits: Incomplete  # DATA DESCRIPTOR

    num_qubits: Incomplete  # DATA DESCRIPTOR

    op: Incomplete  # DATA DESCRIPTOR

    params: Incomplete  # DATA DESCRIPTOR

    qargs: Incomplete  # DATA DESCRIPTOR


class DAGOutNode(DAGNode):
    """Object to represent an outgoing wire node in the DAGCircuit."""

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getstate__(self, /):
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __setstate__(self, /, state):
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    _node_id: Incomplete  # DATA DESCRIPTOR

    wire: Incomplete  # DATA DESCRIPTOR


class Duration:
    """A length of time used to express circuit timing.

    It defines a group of classes which are all subclasses of itself (functionally, an
    enumeration carrying data).

    In Python 3.10+, you can use it in a match statement::

      match duration:
         case Duration.dt(dt):
             return dt
         case Duration.s(seconds):
             return seconds / 5e-7
         case _:
             raise ValueError("expected dt or seconds")

    And in Python 3.9, you can use :meth:`Duration.unit` to determine which variant
    is populated::

      if duration.unit() == "dt":
          return duration.value()
      elif duration.unit() == "s":
          return duration.value() / 5e-7
      else:
          raise ValueError("expected dt or seconds")"""

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...


    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    dt: type

    ms: type

    ns: type

    ps: type

    s: type

    def unit(self, /):
        """The corresponding ``unit`` of the duration."""
        ...

    us: type

    def value(self, /):
        """The ``value`` of the duration.

        This will be a Python ``int`` if the :meth:`~Duration.unit` is ``"dt"``,
        else a ``float``."""
        ...


class Duration_dt(Duration):
    """"""

    _0: Incomplete  # DATA DESCRIPTOR

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getitem__(self, key, /):
        """Return self[key]."""
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...


    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __len__(self, /):
        """Return len(self)."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    __match_args__: tuple

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    dt: type

    ms: type

    ns: type

    ps: type

    s: type

    def unit(self, /):
        """The corresponding ``unit`` of the duration."""
        ...

    us: type

    def value(self, /):
        """The ``value`` of the duration.

        This will be a Python ``int`` if the :meth:`~Duration.unit` is ``"dt"``,
        else a ``float``."""
        ...

    def __iter__(self):
        """make_stubs: MOCKED TO REGISTER THIS CLASS AS AN OLD-STYLE ITERABLE!"""
        ...


class Duration_ms(Duration):
    """"""

    _0: Incomplete  # DATA DESCRIPTOR

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getitem__(self, key, /):
        """Return self[key]."""
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...


    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __len__(self, /):
        """Return len(self)."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    __match_args__: tuple

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    dt: type

    ms: type

    ns: type

    ps: type

    s: type

    def unit(self, /):
        """The corresponding ``unit`` of the duration."""
        ...

    us: type

    def value(self, /):
        """The ``value`` of the duration.

        This will be a Python ``int`` if the :meth:`~Duration.unit` is ``"dt"``,
        else a ``float``."""
        ...

    def __iter__(self):
        """make_stubs: MOCKED TO REGISTER THIS CLASS AS AN OLD-STYLE ITERABLE!"""
        ...


class Duration_ns(Duration):
    """"""

    _0: Incomplete  # DATA DESCRIPTOR

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getitem__(self, key, /):
        """Return self[key]."""
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...


    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __len__(self, /):
        """Return len(self)."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    __match_args__: tuple

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    dt: type

    ms: type

    ns: type

    ps: type

    s: type

    def unit(self, /):
        """The corresponding ``unit`` of the duration."""
        ...

    us: type

    def value(self, /):
        """The ``value`` of the duration.

        This will be a Python ``int`` if the :meth:`~Duration.unit` is ``"dt"``,
        else a ``float``."""
        ...

    def __iter__(self):
        """make_stubs: MOCKED TO REGISTER THIS CLASS AS AN OLD-STYLE ITERABLE!"""
        ...


class Duration_ps(Duration):
    """"""

    _0: Incomplete  # DATA DESCRIPTOR

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getitem__(self, key, /):
        """Return self[key]."""
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...


    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __len__(self, /):
        """Return len(self)."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    __match_args__: tuple

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    dt: type

    ms: type

    ns: type

    ps: type

    s: type

    def unit(self, /):
        """The corresponding ``unit`` of the duration."""
        ...

    us: type

    def value(self, /):
        """The ``value`` of the duration.

        This will be a Python ``int`` if the :meth:`~Duration.unit` is ``"dt"``,
        else a ``float``."""
        ...

    def __iter__(self):
        """make_stubs: MOCKED TO REGISTER THIS CLASS AS AN OLD-STYLE ITERABLE!"""
        ...


class Duration_s(Duration):
    """"""

    _0: Incomplete  # DATA DESCRIPTOR

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getitem__(self, key, /):
        """Return self[key]."""
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...


    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __len__(self, /):
        """Return len(self)."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    __match_args__: tuple

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    dt: type

    ms: type

    ns: type

    ps: type

    s: type

    def unit(self, /):
        """The corresponding ``unit`` of the duration."""
        ...

    us: type

    def value(self, /):
        """The ``value`` of the duration.

        This will be a Python ``int`` if the :meth:`~Duration.unit` is ``"dt"``,
        else a ``float``."""
        ...

    def __iter__(self):
        """make_stubs: MOCKED TO REGISTER THIS CLASS AS AN OLD-STYLE ITERABLE!"""
        ...


class Duration_us(Duration):
    """"""

    _0: Incomplete  # DATA DESCRIPTOR

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getitem__(self, key, /):
        """Return self[key]."""
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...


    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __len__(self, /):
        """Return len(self)."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    __match_args__: tuple

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    dt: type

    ms: type

    ns: type

    ps: type

    s: type

    def unit(self, /):
        """The corresponding ``unit`` of the duration."""
        ...

    us: type

    def value(self, /):
        """The ``value`` of the duration.

        This will be a Python ``int`` if the :meth:`~Duration.unit` is ``"dt"``,
        else a ``float``."""
        ...

    def __iter__(self):
        """make_stubs: MOCKED TO REGISTER THIS CLASS AS AN OLD-STYLE ITERABLE!"""
        ...


class OPReplay:
    """"""

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getnewargs__(self, /):
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        """Helper for pickle."""
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    lhs: Incomplete  # DATA DESCRIPTOR

    op: Incomplete  # DATA DESCRIPTOR

    rhs: Incomplete  # DATA DESCRIPTOR


class OpCode:
    """"""

    ABS: OpCode

    ACOS: OpCode

    ADD: OpCode

    ASIN: OpCode

    ATAN: OpCode

    CONJ: OpCode

    COS: OpCode

    DIV: OpCode

    EXP: OpCode

    GRAD: OpCode

    LOG: OpCode

    MUL: OpCode

    POW: OpCode

    RDIV: OpCode

    RPOW: OpCode

    RSUB: OpCode

    SIGN: OpCode

    SIN: OpCode

    SUB: OpCode

    SUBSTITUTE: OpCode

    TAN: OpCode

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getnewargs__(self, /):
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __int__(self, /):
        """int(self)"""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        """Helper for pickle."""
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...


class Parameter(ParameterExpression):
    """A compile-time symbolic parameter.

    The value of a :class:`.Parameter` must be entirely determined before a circuit begins execution.
    Typically this will mean that you should supply values for all :class:`.Parameter` s in a
    circuit using :meth:`.QuantumCircuit.assign_parameters`, though certain hardware vendors may
    allow you to give them a circuit in terms of these parameters, provided you also pass the values
    separately.

    This is the atom of :class:`.ParameterExpression`, and is itself an expression.  The numeric
    value of a parameter need not be fixed while the circuit is being defined.

    Examples:

        Construct a variable-rotation X gate using circuit parameters.

        .. plot::
            :alt: Circuit diagram output by the previous code.
            :include-source:

            from qiskit.circuit import QuantumCircuit, Parameter

            # create the parameter
            phi = Parameter("phi")
            qc = QuantumCircuit(1)

            # parameterize the rotation
            qc.rx(phi, 0)
            qc.draw("mpl")

            # bind the parameters after circuit to create a bound circuit
            bc = qc.assign_parameters({phi: 3.14})
            bc.measure_all()
            bc.draw("mpl")"""

    def __abs__(self, /):
        """abs(self)"""
        ...

    def __add__(self, value, /):
        """Return self+value."""
        ...

    def __complex__(self, /):
        ...

    def __copy__(self, /):
        ...

    def __deepcopy__(self, /, _memo):
        ...

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __float__(self, /):
        """float(self)"""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getnewargs__(self, /):
        ...

    def __getstate__(self, /):
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __int__(self, /):
        """int(self)"""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __mul__(self, value, /):
        """Return self*value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __neg__(self, /):
        """-self"""
        ...

    def __pos__(self, /):
        """+self"""
        ...

    def __pow__(self, value, mod=None, /):
        """Return pow(self, value, mod)."""
        ...

    def __radd__(self, value, /):
        """Return value+self."""
        ...

    def __reduce__(self, /):
        """Helper for pickle."""
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __rmul__(self, value, /):
        """Return value*self."""
        ...

    def __rpow__(self, value, mod=None, /):
        """Return pow(value, self, mod)."""
        ...

    def __rsub__(self, value, /):
        """Return value-self."""
        ...

    def __rtruediv__(self, value, /):
        """Return value/self."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __setstate__(self, /, state):
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    def __sub__(self, value, /):
        """Return self-value."""
        ...

    def __truediv__(self, value, /):
        """Return self/value."""
        ...

    _qpy_replay: Incomplete  # DATA DESCRIPTOR

    def _values(self, /):
        """Return all values in this equation."""
        ...

    def abs(self, /):
        """Take the absolute value of the expression."""
        ...

    def arccos(self, /):
        """Arccosine of the expression."""
        ...

    def arcsin(self, /):
        """Arcsine of the expression."""
        ...

    def arctan(self, /):
        """Arctangent of the expression."""
        ...

    def assign(self, /, parameter, value):
        ...

    def bind(self, /, parameter_values, allow_unknown_parameters=False):
        ...

    def bind_all(self, /, values):
        ...

    def conjugate(self, /):
        """Return the complex conjugate of the expression."""
        ...

    def cos(self, /):
        """Cosine of the expression."""
        ...

    def exp(self, /):
        """Exponentiate the expression."""
        ...

    def gradient(self, /, param):
        """Return derivative of this expression with respect to the input parameter.

        Args:
            param: The parameter with respect to which the derivative is calculated.

        Returns:
            The derivative as either a constant numeric value or a symbolic
            :class:`.ParameterExpression`."""
        ...

    def is_real(self, /):
        """Check whether the expression represents a real number.

        Note that this will return ``None`` if there are unbound parameters, in which case
        it cannot be determined whether the expression is real."""
        ...

    def is_symbol(self, /):
        """Check if the expression corresponds to a plain symbol.

        Returns:
            ``True`` is this expression corresponds to a symbol, ``False`` otherwise."""
        ...

    def log(self, /):
        """Take the natural logarithm of the expression."""
        ...

    name: Incomplete  # DATA DESCRIPTOR
    """Returns the name of the :class:`.Parameter`."""

    def numeric(self, /, strict=True):
        """Cast this expression to a numeric value.

        Args:
            strict: If ``True`` (default) this function raises an error if there are any
                unbound symbols in the expression. If ``False``, this allows casting
                if the expression represents a numeric value, regardless of unbound symbols.
                For example ``(0 * Parameter("x"))`` is 0 but has the symbol ``x`` present."""
        ...

    parameters: Incomplete  # DATA DESCRIPTOR
    """Get the parameters present in the expression.

    .. note::

        Qiskit guarantees equality (via ``==``) of parameters retrieved from an expression
        with the original :class:`.Parameter` objects used to create this expression,
        but does **not guarantee** ``is`` comparisons to succeed.
    """

    def sign(self, /):
        """Return the sign of the expression."""
        ...

    def sin(self, /):
        """Sine of the expression."""
        ...

    def subs(self, /, parameter_map, allow_unknown_parameters=False):
        ...

    def sympify(self, /):
        """Return a SymPy equivalent of this expression.

        Returns:
            A SymPy equivalent of this expression."""
        ...

    def tan(self, /):
        """Tangent of the expression."""
        ...

    uuid: Incomplete  # DATA DESCRIPTOR
    """Returns the :class:`~uuid.UUID` of the :class:`Parameter`.

    In advanced use cases, this property can be passed to the
    :class:`.Parameter` constructor to produce an instance that compares
    equal to another instance."""


class ParameterExpression:
    """A parameter expression.

    This is backed by Qiskit's symbolic expression engine and a cache
    for the parameters inside the expression."""

    def __abs__(self, /):
        """abs(self)"""
        ...

    def __add__(self, value, /):
        """Return self+value."""
        ...

    def __complex__(self, /):
        ...

    def __copy__(self, /):
        ...

    def __deepcopy__(self, /, _memo):
        ...

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __float__(self, /):
        """float(self)"""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getstate__(self, /):
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __int__(self, /):
        """int(self)"""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __mul__(self, value, /):
        """Return self*value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __neg__(self, /):
        """-self"""
        ...

    def __pos__(self, /):
        """+self"""
        ...

    def __pow__(self, value, mod=None, /):
        """Return pow(self, value, mod)."""
        ...

    def __radd__(self, value, /):
        """Return value+self."""
        ...

    def __reduce__(self, /):
        """Helper for pickle."""
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __rmul__(self, value, /):
        """Return value*self."""
        ...

    def __rpow__(self, value, mod=None, /):
        """Return pow(value, self, mod)."""
        ...

    def __rsub__(self, value, /):
        """Return value-self."""
        ...

    def __rtruediv__(self, value, /):
        """Return value/self."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __setstate__(self, /, state):
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    def __sub__(self, value, /):
        """Return self-value."""
        ...

    def __truediv__(self, value, /):
        """Return self/value."""
        ...

    _qpy_replay: Incomplete  # DATA DESCRIPTOR

    def _values(self, /):
        """Return all values in this equation."""
        ...

    def abs(self, /):
        """Take the absolute value of the expression."""
        ...

    def arccos(self, /):
        """Arccosine of the expression."""
        ...

    def arcsin(self, /):
        """Arcsine of the expression."""
        ...

    def arctan(self, /):
        """Arctangent of the expression."""
        ...

    def assign(self, /, parameter, value):
        """Assign one parameter to a value, which can either be numeric or another parameter
        expression.

        Args:
            parameter: A parameter in this expression whose value will be updated.
            value: The new value to bind to.

        Returns:
            A new expression parameterized by any parameters which were not bound by assignment."""
        ...

    def bind(self, /, parameter_values, allow_unknown_parameters=False):
        """Binds the provided set of parameters to their corresponding values.

        Args:
            parameter_values: Mapping of :class:`.Parameter` instances to the numeric value to which
                they will be bound.
            allow_unknown_parameters: If ``False``, raises an error if ``parameter_values``
                contains :class:`.Parameter` s in the keys outside those present in the expression.
                If ``True``, any such parameters are simply ignored.

        Raises:
            CircuitError:
                - If parameter_values contains parameters outside those in self.
                - If a non-numeric value is passed in ``parameter_values``.
            ZeroDivisionError:
                - If binding the provided values requires division by zero.

        Returns:
            A new expression parameterized by any parameters which were not bound by
            ``parameter_values``."""
        ...

    def bind_all(self, /, values):
        """Bind all of the parameters in ``self`` to numeric values in the dictionary, returning a
        numeric value.

        This is a special case of :meth:`bind` which can reach higher performance.  It is no problem
        for the ``values`` dictionary to contain parameters that are not used in this expression;
        the expectation is that the same bindings dictionary will be fed to other expressions as
        well.

        It is an error to call this method with a ``values`` dictionary that does not bind all of
        the values, or to call this method with non-numeric values, but this is not explicitly
        checked, since this method is intended for performance-sensitive use.  Passing an incorrect
        dictionary may result in unexpected behavior.

        Unlike :meth:`bind`, this method will not raise an exception if non-finite floating-point
        values are encountered.

        Args:
            values: mapping of parameters to numeric values."""
        ...

    def conjugate(self, /):
        """Return the complex conjugate of the expression."""
        ...

    def cos(self, /):
        """Cosine of the expression."""
        ...

    def exp(self, /):
        """Exponentiate the expression."""
        ...

    def gradient(self, /, param):
        """Return derivative of this expression with respect to the input parameter.

        Args:
            param: The parameter with respect to which the derivative is calculated.

        Returns:
            The derivative as either a constant numeric value or a symbolic
            :class:`.ParameterExpression`."""
        ...

    def is_real(self, /):
        """Check whether the expression represents a real number.

        Note that this will return ``None`` if there are unbound parameters, in which case
        it cannot be determined whether the expression is real."""
        ...

    def is_symbol(self, /):
        """Check if the expression corresponds to a plain symbol.

        Returns:
            ``True`` is this expression corresponds to a symbol, ``False`` otherwise."""
        ...

    def log(self, /):
        """Take the natural logarithm of the expression."""
        ...

    def numeric(self, /, strict=True):
        """Cast this expression to a numeric value.

        Args:
            strict: If ``True`` (default) this function raises an error if there are any
                unbound symbols in the expression. If ``False``, this allows casting
                if the expression represents a numeric value, regardless of unbound symbols.
                For example ``(0 * Parameter("x"))`` is 0 but has the symbol ``x`` present."""
        ...

    parameters: Incomplete  # DATA DESCRIPTOR
    """Get the parameters present in the expression.

    .. note::

        Qiskit guarantees equality (via ``==``) of parameters retrieved from an expression
        with the original :class:`.Parameter` objects used to create this expression,
        but does **not guarantee** ``is`` comparisons to succeed.
    """

    def sign(self, /):
        """Return the sign of the expression."""
        ...

    def sin(self, /):
        """Sine of the expression."""
        ...

    def subs(self, /, parameter_map, allow_unknown_parameters=False):
        """Returns a new expression with replacement parameters.

        Args:
            parameter_map: Mapping from :class:`.Parameter` s in ``self`` to the
                :class:`.ParameterExpression` instances with which they should be replaced.
            allow_unknown_parameters: If ``False``, raises an error if ``parameter_map``
                contains :class:`.Parameter` s in the keys outside those present in the expression.
                If ``True``, any such parameters are simply ignored.

        Raises:
            CircuitError:
                - If parameter_map contains parameters outside those in self.
                - If the replacement parameters in ``parameter_map`` would result in
                  a name conflict in the generated expression.

        Returns:
            A new expression with the specified parameters replaced."""
        ...

    def sympify(self, /):
        """Return a SymPy equivalent of this expression.

        Returns:
            A SymPy equivalent of this expression."""
        ...

    def tan(self, /):
        """Tangent of the expression."""
        ...


class ParameterVectorElement(Parameter):
    """An element of a :class:`.ParameterVector`.

    .. note::
        There is very little reason to ever construct this class directly.  Objects of this type are
        automatically constructed efficiently as part of creating a :class:`.ParameterVector`."""

    def __abs__(self, /):
        """abs(self)"""
        ...

    def __add__(self, value, /):
        """Return self+value."""
        ...

    def __complex__(self, /):
        ...

    def __copy__(self, /):
        ...

    def __deepcopy__(self, /, _memo):
        ...

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __float__(self, /):
        """float(self)"""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getnewargs__(self, /):
        ...

    def __getstate__(self, /):
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __int__(self, /):
        """int(self)"""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __mul__(self, value, /):
        """Return self*value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __neg__(self, /):
        """-self"""
        ...

    def __pos__(self, /):
        """+self"""
        ...

    def __pow__(self, value, mod=None, /):
        """Return pow(self, value, mod)."""
        ...

    def __radd__(self, value, /):
        """Return value+self."""
        ...

    def __reduce__(self, /):
        """Helper for pickle."""
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __rmul__(self, value, /):
        """Return value*self."""
        ...

    def __rpow__(self, value, mod=None, /):
        """Return pow(value, self, mod)."""
        ...

    def __rsub__(self, value, /):
        """Return value-self."""
        ...

    def __rtruediv__(self, value, /):
        """Return value/self."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __setstate__(self, /, state):
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    def __sub__(self, value, /):
        """Return self-value."""
        ...

    def __truediv__(self, value, /):
        """Return self/value."""
        ...

    _qpy_replay: Incomplete  # DATA DESCRIPTOR

    def _values(self, /):
        """Return all values in this equation."""
        ...

    _vector: Incomplete  # DATA DESCRIPTOR
    """For backward compatibility only. This should not be used and we ought to update those
    usages!"""

    def abs(self, /):
        """Take the absolute value of the expression."""
        ...

    def arccos(self, /):
        """Arccosine of the expression."""
        ...

    def arcsin(self, /):
        """Arcsine of the expression."""
        ...

    def arctan(self, /):
        """Arctangent of the expression."""
        ...

    def assign(self, /, parameter, value):
        ...

    def bind(self, /, parameter_values, allow_unknown_parameters=False):
        ...

    def bind_all(self, /, values):
        ...

    def conjugate(self, /):
        """Return the complex conjugate of the expression."""
        ...

    def cos(self, /):
        """Cosine of the expression."""
        ...

    def exp(self, /):
        """Exponentiate the expression."""
        ...

    def gradient(self, /, param):
        """Return derivative of this expression with respect to the input parameter.

        Args:
            param: The parameter with respect to which the derivative is calculated.

        Returns:
            The derivative as either a constant numeric value or a symbolic
            :class:`.ParameterExpression`."""
        ...

    index: Incomplete  # DATA DESCRIPTOR
    """Get the index of this element in the parent vector."""

    def is_real(self, /):
        """Check whether the expression represents a real number.

        Note that this will return ``None`` if there are unbound parameters, in which case
        it cannot be determined whether the expression is real."""
        ...

    def is_symbol(self, /):
        """Check if the expression corresponds to a plain symbol.

        Returns:
            ``True`` is this expression corresponds to a symbol, ``False`` otherwise."""
        ...

    def log(self, /):
        """Take the natural logarithm of the expression."""
        ...

    name: Incomplete  # DATA DESCRIPTOR
    """Returns the name of the :class:`.Parameter`."""

    def numeric(self, /, strict=True):
        """Cast this expression to a numeric value.

        Args:
            strict: If ``True`` (default) this function raises an error if there are any
                unbound symbols in the expression. If ``False``, this allows casting
                if the expression represents a numeric value, regardless of unbound symbols.
                For example ``(0 * Parameter("x"))`` is 0 but has the symbol ``x`` present."""
        ...

    parameters: Incomplete  # DATA DESCRIPTOR
    """Get the parameters present in the expression.

    .. note::

        Qiskit guarantees equality (via ``==``) of parameters retrieved from an expression
        with the original :class:`.Parameter` objects used to create this expression,
        but does **not guarantee** ``is`` comparisons to succeed.
    """

    def sign(self, /):
        """Return the sign of the expression."""
        ...

    def sin(self, /):
        """Sine of the expression."""
        ...

    def subs(self, /, parameter_map, allow_unknown_parameters=False):
        ...

    def sympify(self, /):
        """Return a SymPy equivalent of this expression.

        Returns:
            A SymPy equivalent of this expression."""
        ...

    def tan(self, /):
        """Tangent of the expression."""
        ...

    uuid: Incomplete  # DATA DESCRIPTOR
    """Returns the :class:`~uuid.UUID` of the :class:`Parameter`.

    In advanced use cases, this property can be passed to the
    :class:`.Parameter` constructor to produce an instance that compares
    equal to another instance."""

    vector: Incomplete  # DATA DESCRIPTOR
    """Get the parent vector instance."""


class QuantumRegister(Register):
    """Implement a register."""

    def __contains__(self, key, /):
        """Return bool(key in self)."""
        ...

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getitem__(self, key, /):
        """Return self[key]."""
        ...

    def __getnewargs__(self, /):
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __len__(self, /):
        """Return len(self)."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        """Helper for pickle."""
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    bit_type: type

    def index(self, /, bit):
        """The index of the given bit in the register."""
        ...

    instances_count: int

    name: Incomplete  # DATA DESCRIPTOR
    """The name of the register."""

    prefix: str

    size: Incomplete  # DATA DESCRIPTOR
    """The size of the register."""

    def __iter__(self):
        """make_stubs: MOCKED TO REGISTER THIS CLASS AS AN OLD-STYLE ITERABLE!"""
        ...


class Qubit(Bit):
    """A qubit, which can be compared between different circuits."""

    def __copy__(self, /):
        ...

    def __deepcopy__(self, /, _memo):
        ...

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    _index: Incomplete  # DATA DESCRIPTOR

    _register: Incomplete  # DATA DESCRIPTOR


class Register:
    """Implement a generic register.

    .. note::
        This class cannot be instantiated directly.  Its only purpose is to allow generic type
        checking for :class:`~.ClassicalRegister` and :class:`~.QuantumRegister`."""

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        """Helper for pickle."""
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...


class StandardGate:
    """None"""

    C3SX: StandardGate

    C3X: StandardGate

    CCX: StandardGate

    CCZ: StandardGate

    CH: StandardGate

    CPhase: StandardGate

    CRX: StandardGate

    CRY: StandardGate

    CRZ: StandardGate

    CS: StandardGate

    CSX: StandardGate

    CSdg: StandardGate

    CSwap: StandardGate

    CU: StandardGate

    CU1: StandardGate

    CU3: StandardGate

    CX: StandardGate

    CY: StandardGate

    CZ: StandardGate

    DCX: StandardGate

    ECR: StandardGate

    GlobalPhase: StandardGate

    H: StandardGate

    I: StandardGate

    ISwap: StandardGate

    Phase: StandardGate

    R: StandardGate

    RC3X: StandardGate

    RCCX: StandardGate

    RX: StandardGate

    RXX: StandardGate

    RY: StandardGate

    RYY: StandardGate

    RZ: StandardGate

    RZX: StandardGate

    RZZ: StandardGate

    S: StandardGate

    SX: StandardGate

    SXdg: StandardGate

    Sdg: StandardGate

    Swap: StandardGate

    T: StandardGate

    Tdg: StandardGate

    U: StandardGate

    U1: StandardGate

    U2: StandardGate

    U3: StandardGate

    X: StandardGate

    XXMinusYY: StandardGate

    XXPlusYY: StandardGate

    Y: StandardGate

    Z: StandardGate

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...

    def __hash__(self, /):
        """Return hash(self)."""
        ...

    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __int__(self, /):
        """int(self)"""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        """Helper for pickle."""
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...

    def _get_definition(self, /, params):
        ...

    def _inverse(self, /, params):
        ...

    def _num_params(self, /):
        ...

    def _to_matrix(self, /, params):
        ...

    def copy(self, /):
        ...

    gate_class: Incomplete  # DATA DESCRIPTOR

    is_controlled_gate: Incomplete  # DATA DESCRIPTOR

    name: Incomplete  # DATA DESCRIPTOR

    num_clbits: Incomplete  # DATA DESCRIPTOR

    num_ctrl_qubits: Incomplete  # DATA DESCRIPTOR

    num_params: Incomplete  # DATA DESCRIPTOR

    num_qubits: Incomplete  # DATA DESCRIPTOR


class StandardInstructionType:
    """An internal type used to further discriminate the payload of a `PackedOperation` when its
    discriminant is `PackedOperationType::StandardInstruction`.

    This is also used to tag standard instructions via the `_standard_instruction_type` class
    attribute in the corresponding Python class."""

    Barrier: StandardInstructionType

    Delay: StandardInstructionType

    Measure: StandardInstructionType

    Reset: StandardInstructionType

    def __delattr__(self, name, /):
        """Implement delattr(self, name)."""
        ...

    def __dir__(self, /):
        """Default dir() implementation."""
        ...

    def __eq__(self, value, /):
        """Return self==value."""
        ...

    def __format__(self, format_spec, /):
        """Default object formatter.

        Return str(self) if format_spec is empty. Raise TypeError otherwise."""
        ...

    def __ge__(self, value, /):
        """Return self>=value."""
        ...

    def __getattribute__(self, name, /):
        """Return getattr(self, name)."""
        ...

    def __getstate__(self, /):
        """Helper for pickle."""
        ...

    def __gt__(self, value, /):
        """Return self>value."""
        ...


    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __int__(self, /):
        """int(self)"""
        ...

    def __le__(self, value, /):
        """Return self<=value."""
        ...

    def __lt__(self, value, /):
        """Return self<value."""
        ...

    def __ne__(self, value, /):
        """Return self!=value."""
        ...

    def __reduce__(self, /):
        """Helper for pickle."""
        ...

    def __reduce_ex__(self, protocol, /):
        """Helper for pickle."""
        ...

    def __repr__(self, /):
        """Return repr(self)."""
        ...

    def __setattr__(self, name, value, /):
        """Implement setattr(self, name, value)."""
        ...

    def __sizeof__(self, /):
        """Size of object in memory, in bytes."""
        ...

    def __str__(self, /):
        """Return str(self)."""
        ...
