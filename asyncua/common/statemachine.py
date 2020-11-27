import asyncio, logging

from asyncua import Server, ua, Node
from asyncua.common.instantiate_util import instantiate

class StateMachineTypeClass(object):
    '''
    Implementation of an StateMachineType
    '''
    def __init__(self, server=None, parent=None, idx=None, name=None):
        if not server: raise ValueError #change to check instance type
        if not parent: raise ValueError #change to check instance type
        if idx == None:
            idx = parent.nodeid.NamespaceIndex
        if name == None:
            name = "StateMachine"
        self._server = server
        self._parent = parent
        self._state_machine_node = None
        self._state_machine_type = ua.NodeId(2299, 0)
        self._name = name
        self._idx = idx
        self._optionals = False
        self._current_state_node = None
        self._current_state_id_node = None
        self._last_transition_node = None
        self._last_transition_node_id = None

    async def install(self, optionals=False):
        '''
        setup adressspace and initialize 
        '''
        self._optionals = optionals
        self._state_machine_node = await self._parent.add_object(self._idx, self._name, objecttype=self._state_machine_type, instantiate_optional=optionals)
        self._current_state_node = await self._state_machine_node.get_child(["CurrentState"])
        self._current_state_id_node = await self._state_machine_node.get_child(["CurrentState","Id"])
        if self._optionals:
            self._current_transition_node = await self._state_machine_node.get_child(["LastTransition"])
            self._current_transition_id_node = await self._state_machine_node.get_child(["LastTransition","Id"])
        
        #initialise values
        #maybe its smart to check parents child for a initial state instance (InitialStateType) and initialize it with its id but if no state instance is brovided ...
        
    async def change_state(self, state_name, state_node, transition_name=None, transition_node=None):
        '''
        state_name: ua.LocalizedText()
        state: ua.NodeId() <- StateType node
        transition_name: ua.LocalizedText()
        transition: ua.NodeId() <- TransitionType node
        '''
        #check types/class
        #check StateType exist
        #check TransitionTypeType exist
        await self.write_state(state_name, state_node)
        if self._optionals and transition_name and transition_node:
            await self.write_transition(transition_name, transition_node)

    async def write_state(self, state_name, state_node):
        #check types/class
        await self._current_state_node.write_value(state_name)
        await self._current_state_id_node.write_value(state_node)

    async def write_transition(self, transition_name, transition_node):
        #check types/class
        await self._last_transition_node.write_value(transition_name)
        await self._last_transition_id_node.write_value(transition_node)

class FiniteStateMachineTypeClass(StateMachineTypeClass):
    '''
    Implementation of an FiniteStateMachineType
    '''
    def __init__(self, server=None, parent=None, idx=None, name=None):
        super().__init__(server, parent, idx, name)
        if name == None:
            name = "FiniteStateMachine"
        self._state_machine_type = ua.NodeId(2771, 0)
        self._avalible_states = []
        self._avalible_transitions = []

    async def install(self, optionals=False):
        '''
        setup adressspace and initialize 
        '''
        self._optionals = optionals
        self._state_machine_node = await self._parent.add_object(self._idx, self._name, objecttype=self._state_machine_type, instantiate_optional=optionals)

    async def set_avalible_states(self, states):
        self._avalible_states = states

    async def set_avalible_transitions(self, transitions):
        self._avalible_transitions = transitions      

class ExclusiveLimitStateMachineTypeClass(FiniteStateMachineTypeClass):
    '''
    NOT IMPLEMENTED "ExclusiveLimitStateMachineType"
    '''
    def __init__(self, server=None, parent=None, idx=None, name=None):
        super().__init__(server, parent)
        if name == None:
            name = "ExclusiveLimitStateMachine"
        self._state_machine_type = ua.NodeId(9318, 0)
        raise NotImplementedError

class FileTransferStateMachineTypeClass(FiniteStateMachineTypeClass):
    '''
    NOT IMPLEMENTED "FileTransferStateMachineType"
    '''
    def __init__(self, server=None, parent=None, idx=None, name=None):
        super().__init__(server, parent)
        if name == None:
            name = "FileTransferStateMachine"
        self._state_machine_type = ua.NodeId(15803, 0)
        raise NotImplementedError

class ProgramStateMachineTypeClass(FiniteStateMachineTypeClass):
    '''
    https://reference.opcfoundation.org/v104/Core/docs/Part10/4.2.3/
    '''
    def __init__(self, server=None, parent=None, idx=None, name=None):
        super().__init__(server, parent, idx, name)
        if name == None:
            name = "ProgramStateMachine"
        self._state_machine_type = ua.NodeId(2391, 0)
        self._ready_state = None #State node
        self._halted_state = None #State node
        self._running_state = None #State node
        self._suspended_state = None #State node

        self._halted_to_ready = None #Transition node
        self._ready_to_running = None #Transition node
        self._running_to_halted = None #Transition node
        self._running_to_ready = None #Transition node
        self._running_to_suspended = None #Transition node
        self._suspended_to_running = None #Transition node
        self._suspended_to_halted = None #Transition node
        self._suspended_to_ready = None #Transition node
        self._ready_to_halted = None #Transition node

        self._halt_method_node = None #uamethod node
        self._reset_method_node = None #uamethod node
        self._resume_method_node = None #uamethod node
        self._start_method_node = None #uamethod node
        self._suspend_method_node = None #uamethod node

    async def install(self, optionals=False):
        '''
        setup adressspace and initialize 
        '''
        self._optionals = optionals
        self._state_machine_node = await self._parent.add_object(self._idx, self._name, objecttype=self._state_machine_type, instantiate_optional=optionals)
        #get childnodes:
        self._ready_state = None #State node
        self._halted_state = None #State node
        self._running_state = None #State node
        self._suspended_state = None #State node
        self._halted_to_ready = None #Transition node
        self._ready_to_running = None #Transition node
        self._running_to_halted = None #Transition node
        self._running_to_ready = None #Transition node
        self._running_to_suspended = None #Transition node
        self._suspended_to_running = None #Transition node
        self._suspended_to_halted = None #Transition node
        self._suspended_to_ready = None #Transition node
        self._ready_to_halted = None #Transition node
        self._halt_method_node = None #uamethod node
        self._reset_method_node = None #uamethod node
        self._resume_method_node = None #uamethod node
        self._start_method_node = None #uamethod node
        self._suspend_method_node = None #uamethod node

    #Transition
    async def HaltedToReady(self):
        await self._current_state.write_value(ua.LocalizedText("Ready", "en-US"), varianttype=ua.VariantType.LocalizedText)
        await self._current_state_id.write_value(self._ready_state.nodeid, varianttype=ua.VariantType.NodeId)
        await self._last_transition.write_value(ua.LocalizedText("HaltedToReady", "en-US"), varianttype=ua.VariantType.LocalizedText)
        await self._last_transition_id.write_value(self._halted_to_ready.nodeid, varianttype=ua.VariantType.NodeId)
        return ua.StatusCode(ua.status_codes.StatusCodes.Good)

    #Transition
    async def ReadyToRunning(self):
        await self._current_state.write_value(ua.LocalizedText("Running", "en-US"), varianttype=ua.VariantType.LocalizedText)
        await self._current_state_id.write_value(self._running_state.nodeid, varianttype=ua.VariantType.NodeId)
        await self._last_transition.write_value(ua.LocalizedText("ReadyToRunning", "en-US"), varianttype=ua.VariantType.LocalizedText)
        await self._last_transition_id.write_value(self._ready_to_running.nodeid, varianttype=ua.VariantType.NodeId)
        return ua.StatusCode(ua.status_codes.StatusCodes.Good)

    #Transition
    async def RunningToHalted(self):
        await self._current_state.write_value(ua.LocalizedText("Halted", "en-US"), varianttype=ua.VariantType.LocalizedText)
        await self._current_state_id.write_value(self._halted_state.nodeid, varianttype=ua.VariantType.NodeId)
        await self._last_transition.write_value(ua.LocalizedText("RunningToHalted", "en-US"), varianttype=ua.VariantType.LocalizedText)
        await self._last_transition_id.write_value(self._running_to_halted.nodeid, varianttype=ua.VariantType.NodeId)
        return ua.StatusCode(ua.status_codes.StatusCodes.Good)

    #Transition
    async def RunningToReady(self):
        await self._current_state.write_value(ua.LocalizedText("Ready", "en-US"), varianttype=ua.VariantType.LocalizedText)
        await self._current_state_id.write_value(self._ready_state.nodeid, varianttype=ua.VariantType.NodeId)
        await self._last_transition.write_value(ua.LocalizedText("RunningToReady", "en-US"), varianttype=ua.VariantType.LocalizedText)
        await self._last_transition_id.write_value(self._running_to_ready.nodeid, varianttype=ua.VariantType.NodeId)
        return ua.StatusCode(ua.status_codes.StatusCodes.Good)

    #Transition
    async def RunningToSuspended(self):
        await self._current_state.write_value(ua.LocalizedText("Suspended", "en-US"), varianttype=ua.VariantType.LocalizedText)
        await self._current_state_id.write_value(self._suspended_state.nodeid, varianttype=ua.VariantType.NodeId)
        await self._last_transition.write_value(ua.LocalizedText("RunningToSuspended", "en-US"), varianttype=ua.VariantType.LocalizedText)
        await self._last_transition_id.write_value(self._running_to_suspended.nodeid, varianttype=ua.VariantType.NodeId)
        return ua.StatusCode(ua.status_codes.StatusCodes.Good)

    #Transition 
    async def SuspendedToRunning(self):
        await self._current_state.write_value(ua.LocalizedText("Running", "en-US"), varianttype=ua.VariantType.LocalizedText)
        await self._current_state_id.write_value(self._running_state.nodeid, varianttype=ua.VariantType.NodeId)
        await self._last_transition.write_value(ua.LocalizedText("SuspendedToRunning", "en-US"), varianttype=ua.VariantType.LocalizedText)
        await self._last_transition_id.write_value(self._suspended_to_running.nodeid, varianttype=ua.VariantType.NodeId)
        return ua.StatusCode(ua.status_codes.StatusCodes.Good)

    #Transition
    async def SuspendedToHalted(self):
        await self._current_state.write_value(ua.LocalizedText("Halted", "en-US"), varianttype=ua.VariantType.LocalizedText)
        await self._current_state_id.write_value(self._halted_state.nodeid, varianttype=ua.VariantType.NodeId)
        await self._last_transition.write_value(ua.LocalizedText("SuspendedToHalted", "en-US"), varianttype=ua.VariantType.LocalizedText)
        await self._last_transition_id.write_value(self._suspended_to_halted.nodeid, varianttype=ua.VariantType.NodeId)
        return ua.StatusCode(ua.status_codes.StatusCodes.Good)

    #Transition
    async def SuspendedToReady(self):
        await self._current_state.write_value(ua.LocalizedText("Ready", "en-US"), varianttype=ua.VariantType.LocalizedText)
        await self._current_state_id.write_value(self._ready_state.nodeid, varianttype=ua.VariantType.NodeId)
        await self._last_transition.write_value(ua.LocalizedText("SuspendedToReady", "en-US"), varianttype=ua.VariantType.LocalizedText)
        await self._last_transition_id.write_value(self._suspended_to_ready.nodeid, varianttype=ua.VariantType.NodeId)
        return ua.StatusCode(ua.status_codes.StatusCodes.Good)

    #Transition 
    async def ReadyToHalted(self):
        await self._current_state.write_value(ua.LocalizedText("Halted", "en-US"), varianttype=ua.VariantType.LocalizedText)
        await self._current_state_id.write_value(self._halted_state.nodeid, varianttype=ua.VariantType.NodeId)
        await self._last_transition.write_value(ua.LocalizedText("ReadyToHalted", "en-US"), varianttype=ua.VariantType.LocalizedText)
        await self._last_transition_id.write_value(self._ready_to_halted.nodeid, varianttype=ua.VariantType.NodeId)
        return ua.StatusCode(ua.status_codes.StatusCodes.Good)

    #method to be linked to uamethod
    async def Start(self):
        if await self._current_state.read_value() == ua.LocalizedText("Ready", "en-US"):
            return await ReadyToRunning()
        else:
            return ua.StatusCode(ua.status_codes.StatusCodes.BadNotExecutable)

    #method to be linked to uamethod
    async def Suspend(self):
        if await self._current_state.read_value() == ua.LocalizedText("Running", "en-US"):
            return await RunningToSuspended()
        else:
            return ua.StatusCode(ua.status_codes.StatusCodes.BadNotExecutable)

    #method to be linked to uamethod
    async def Resume(self):
        if await self._current_state.read_value() == ua.LocalizedText("Suspended", "en-US"):
            return await SuspendedToRunning()
        else:
            return ua.StatusCode(ua.status_codes.StatusCodes.BadNotExecutable)

    #method to be linked to uamethod
    async def Halt(self):
        if await self._current_state.read_value() == ua.LocalizedText("Ready", "en-US"):
            return await ReadyToHalted()
        elif await self._current_state.read_value() == ua.LocalizedText("Running", "en-US"):
            return await RunningToHalted()
        elif await self._current_state.read_value() == ua.LocalizedText("Suspended", "en-US"):
            return await SuspendedToHalted()
        else:
            return ua.StatusCode(ua.status_codes.StatusCodes.BadNotExecutable)

    #method to be linked to uamethod
    async def Reset(self):
        if await self._current_state.read_value() == ua.LocalizedText("Halted", "en-US"):
            return await HaltedToReady()
        else:
            return ua.StatusCode(ua.status_codes.StatusCodes.BadNotExecutable)

class ShelvedStateMachineTypeClass(FiniteStateMachineTypeClass):
    '''
    NOT IMPLEMENTED "ShelvedStateMachineType"
    '''
    def __init__(self, server=None, parent=None, idx=None, name=None):
        super().__init__(server, parent)
        if name == None:
            name = "ShelvedStateMachine"
        self._state_machine_type = ua.NodeId(2929, 0)
        raise NotImplementedError


#Devtests
async def main():
    logging.basicConfig(level=logging.INFO)
    _logger = logging.getLogger('asyncua')

    server = Server()
    await server.init()

    sm = StateMachineTypeClass(server, server.nodes.objects, 0, "StateMachine")
    await sm.install(True)
    await sm.change_state(ua.LocalizedText("Test", "en-US"), server.get_node("ns=0;i=2253").nodeid)
    fsm = FiniteStateMachineTypeClass(server, server.nodes.objects, 0, "FiniteStateMachine")
    await fsm.install(True)
    pfsm = ProgramStateMachineTypeClass(server, server.nodes.objects, 0, "ProgramStateMachine")
    await pfsm.install(True)

    async with server:
        while 1:
            await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())