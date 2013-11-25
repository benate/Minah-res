from Service import Service, PacketHeader
from User import User
from Def import PacketType, Request, Response, Notification
import Def

def isInLocation(expected):
    def new_func(func):
        def decorated(self, request, response):
            if self.user.location == None or self.user.location.type != expected:
                response.result = Response.STATE_INVALID
            else:
                func(self, request, response)
        return decorated
    return new_func


class GameService(Service):
    def doCheckVersion(self, request, response):
        response.result = Response.SUCCESS

    def doLogin(self, request, response):
        nickname = request.login.nickname
        if nickname in self.server.users:
            response.result = Response.LOGIN_DUPLICATED
        else:
            self.user = User(self, nickname)
            self.server.users[nickname] = self.user
            response.result = Response.SUCCESS

    def doChat(self, request, response):
        if request.chat.to in self.server.users:
            noti = Notification()
            noti.type = Notification.CHAT
            noti.chat.to = request.chat.to
            noti.chat.message = request.chat.message
            self.server.users[request.chat.to].notify(noti)
            response.result = Response.SUCCESS
        else:
            response.result = Response.USER_NOT_EXISTS

    def doCreateRoom(self, request, response):
        roomNumber = self.server.roomManager.createRoom(self.user)
        if roomNumber != Def.kInvalidId:
            response.result = Response.SUCCESS
            response.create_room.number = roomNumber
        else:
            response.result = Response.SERVER_BUSY

    def doEnterRoom(self, request, response):
        if not request.HasField("enter_room"):
            response.result = Response.FIELD_MISSING
            return

        number = request.enter_room.number
        response.result = self.server.roomManager.enterRoom(number, self.user)

    @isInLocation(Def.LocationType.kRoom)
    def doStartGame(self, request, response):
        response.result = self.user.location.startGame(self.user)

    @isInLocation(Def.LocationType.kRoom)
    def doReady(self, request, response):
        self.user.location.ready(self.user)
        response.result = Response.SUCCESS

    @isInLocation(Def.LocationType.kRoom)
    def doChangeTurn(self, request, response):
        response.result = self.user.location.changeTurn(self.user)
