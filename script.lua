-- Auto Parry GUI System pentru Blade Ball
-- Design modern cu animații și customizare

-- Services
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local TweenService = game:GetService("TweenService")
local StarterGui = game:GetService("StarterGui")
local VirtualInputManager = game:GetService("VirtualInputManager")

-- Variabile locale
local Player = Players.LocalPlayer
local Mouse = Player:GetMouse()

-- Configurație
local Config = {
    AutoParry = true,
    Visualizer = true,
    ParryDistance = 0.55,
    CooldownTime = 1,
    Prediction = true,
    VisualizerColor = Color3.fromRGB(0, 170, 255),
    VisualizerSize = 15,
    Keybind = Enum.KeyCode.RightShift
}

-- State
local State = {
    ParryCooldown = tick(),
    IsParried = false,
    BallConnection = nil,
    GUIVisible = true,
    Dragging = false,
    DragStart = nil,
    DragObject = nil
}

-- UI Assets
local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "NoEnemiesHubGUI"
ScreenGui.ResetOnSpawn = false
ScreenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling

local MainFrame = Instance.new("Frame")
local TopBar = Instance.new("Frame")
local Title = Instance.new("TextLabel")
local CloseButton = Instance.new("TextButton")
local MinimizeButton = Instance.new("TextButton")
local TabsContainer = Instance.new("Frame")
local ContentContainer = Instance.new("Frame")

-- Funcții utilitare
local function CreateNotification(title, text, icon, duration)
    StarterGui:SetCore("SendNotification", {
        Title = title,
        Text = text,
        Icon = icon,
        Duration = duration,
        Button1 = "OK"
    })
end

local function TweenObject(object, properties, duration, easingStyle, easingDirection)
    local tweenInfo = TweenInfo.new(duration or 0.3, easingStyle or Enum.EasingStyle.Quint, easingDirection or Enum.EasingDirection.Out)
    local tween = TweenService:Create(object, tweenInfo, properties)
    tween:Play()
    return tween
end

-- Funcția pentru obținerea mingii
local function GetBall()
    for _, Ball in ipairs(workspace.Balls:GetChildren()) do
        if Ball:GetAttribute("realBall") then
            return Ball
        end
    end
end

-- Funcția de reset a conexiunii
local function ResetConnection()
    if State.BallConnection then
        State.BallConnection:Disconnect()
        State.BallConnection = nil
    end
end

-- Sistemul de Auto Parry
local function SetupAutoParry()
    -- Conectare la adăugarea de mingi
    workspace.Balls.ChildAdded:Connect(function()
        local Ball = GetBall()
        if not Ball then return end
        ResetConnection()
        State.BallConnection = Ball:GetAttributeChangedSignal("target"):Connect(function()
            State.IsParried = false
        end)
    end)

    -- Loop principal pentru parry
    RunService.PreSimulation:Connect(function()
        if not Config.AutoParry then return end
        
        local Ball = GetBall()
        local Character = Player.Character
        if not Ball or not Character then return end
        
        local HRP = Character:FindFirstChild("HumanoidRootPart")
        if not HRP then return end
        
        local Speed = Ball:FindFirstChild("zoomies") and Ball.zoomies.VectorVelocity.Magnitude or 100
        local Distance = (HRP.Position - Ball.Position).Magnitude
        
        if Ball:GetAttribute("target") == Player.Name and not State.IsParried and Distance / Speed <= Config.ParryDistance then
            -- Execută parry
            VirtualInputManager:SendMouseButtonEvent(0, 0, 0, true, game, 0)
            State.IsParried = true
            State.ParryCooldown = tick()
            
            -- Efect vizual dacă este activat
            if Config.Visualizer then
                spawn(function()
                    -- Creează un efect vizual
                    local visualPart = Instance.new("Part")
                    visualPart.Size = Vector3.new(Config.VisualizerSize, Config.VisualizerSize, Config.VisualizerSize)
                    visualPart.Position = Ball.Position
                    visualPart.Anchored = true
                    visualPart.CanCollide = false
                    visualPart.Material = Enum.Material.Neon
                    visualPart.Color = Config.VisualizerColor
                    visualPart.Transparency = 0.3
                    visualPart.Parent = workspace
                    
                    -- Animație de scalare și transparență
                    for i = 1, 20 do
                        visualPart.Size = visualPart.Size + Vector3.new(1, 1, 1)
                        visualPart.Transparency = visualPart.Transparency + 0.035
                        RunService.RenderStepped:Wait()
                    end
                    visualPart:Destroy()
                end)
            end
        end
        
        -- Reset cooldown
        if (tick() - State.ParryCooldown) >= Config.CooldownTime then
            State.IsParried = false
        end
    end)
end

-- Creare GUI
local function CreateGUI()
    -- Main Frame
    MainFrame.Name = "MainFrame"
    MainFrame.Size = UDim2.new(0, 400, 0, 450)
    MainFrame.Position = UDim2.new(0.5, -200, 0.5, -225)
    MainFrame.BackgroundColor3 = Color3.fromRGB(20, 20, 25)
    MainFrame.BackgroundTransparency = 0.1
    MainFrame.BorderSizePixel = 0
    MainFrame.Parent = ScreenGui
    
    local MainCorner = Instance.new("UICorner")
    MainCorner.CornerRadius = UDim.new(0, 12)
    MainCorner.Parent = MainFrame
    
    local MainStroke = Instance.new("UIStroke")
    MainStroke.Color = Color3.fromRGB(0, 170, 255)
    MainStroke.Thickness = 2
    MainStroke.Parent = MainFrame
    
    -- Top Bar
    TopBar.Name = "TopBar"
    TopBar.Size = UDim2.new(1, 0, 0, 40)
    TopBar.BackgroundColor3 = Color3.fromRGB(15, 15, 20)
    TopBar.BackgroundTransparency = 0.1
    TopBar.BorderSizePixel = 0
    TopBar.Parent = MainFrame
    
    local TopBarCorner = Instance.new("UICorner")
    TopBarCorner.CornerRadius = UDim.new(0, 12)
    TopCorner.CornerRadius = UDim.new(0, 12, 0, 0)
    TopBarCorner.Parent = TopBar
    
    -- Title
    Title.Name = "Title"
    Title.Text = "⚔️ NoEnemies Hub ⚔️"
    Title.Size = UDim2.new(0.6, 0, 1, 0)
    Title.Position = UDim2.new(0.05, 0, 0, 0)
    Title.BackgroundTransparency = 1
    Title.TextColor3 = Color3.fromRGB(255, 255, 255)
    Title.Font = Enum.Font.GothamBold
    Title.TextSize = 18
    Title.TextXAlignment = Enum.TextXAlignment.Left
    Title.Parent = TopBar
    
    -- Close Button
    CloseButton.Name = "CloseButton"
    CloseButton.Text = "×"
    CloseButton.Size = UDim2.new(0, 40, 0, 40)
    CloseButton.Position = UDim2.new(1, -40, 0, 0)
    CloseButton.BackgroundColor3 = Color3.fromRGB(255, 50, 50)
    CloseButton.BackgroundTransparency = 0.8
    CloseButton.TextColor3 = Color3.fromRGB(255, 255, 255)
    CloseButton.Font = Enum.Font.GothamBold
    CloseButton.TextSize = 20
    CloseButton.Parent = TopBar
    
    local CloseCorner = Instance.new("UICorner")
    CloseCorner.CornerRadius = UDim.new(0, 12)
    CloseCorner.Parent = CloseButton
    
    -- Minimize Button
    MinimizeButton.Name = "MinimizeButton"
    MinimizeButton.Text = "─"
    MinimizeButton.Size = UDim2.new(0, 40, 0, 40)
    MinimizeButton.Position = UDim2.new(1, -85, 0, 0)
    MinimizeButton.BackgroundColor3 = Color3.fromRGB(50, 50, 60)
    MinimizeButton.BackgroundTransparency = 0.8
    MinimizeButton.TextColor3 = Color3.fromRGB(255, 255, 255)
    MinimizeButton.Font = Enum.Font.GothamBold
    MinimizeButton.TextSize = 20
    MinimizeButton.Parent = TopBar
    
    local MinimizeCorner = Instance.new("UICorner")
    MinimizeCorner.CornerRadius = UDim.new(0, 12)
    MinimizeCorner.Parent = MinimizeButton
    
    -- Tabs Container
    TabsContainer.Name = "TabsContainer"
    TabsContainer.Size = UDim2.new(1, 0, 0, 50)
    TabsContainer.Position = UDim2.new(0, 0, 0, 40)
    TabsContainer.BackgroundColor3 = Color3.fromRGB(25, 25, 30)
    TabsContainer.BackgroundTransparency = 0.1
    TabsContainer.BorderSizePixel = 0
    TabsContainer.Parent = MainFrame
    
    -- Content Container
    ContentContainer.Name = "ContentContainer"
    ContentContainer.Size = UDim2.new(1, -20, 0, 350)
    ContentContainer.Position = UDim2.new(0, 10, 0, 100)
    ContentContainer.BackgroundTransparency = 1
    ContentContainer.ClipsDescendants = true
    ContentContainer.Parent = MainFrame
    
    -- Funcționalitate pentru butoane
    CloseButton.MouseButton1Click:Connect(function()
        TweenObject(MainFrame, {Size = UDim2.new(0, 0, 0, 0), Position = UDim2.new(0.5, 0, 0.5, 0)}, 0.3)
        wait(0.3)
        ScreenGui:Destroy()
    end)
    
    MinimizeButton.MouseButton1Click:Connect(function()
        if ContentContainer.Visible then
            TweenObject(MainFrame, {Size = UDim2.new(0, 400, 0, 90)}, 0.3)
            ContentContainer.Visible = false
            MinimizeButton.Text = "+"
        else
            TweenObject(MainFrame, {Size = UDim2.new(0, 400, 0, 450)}, 0.3)
            ContentContainer.Visible = true
            MinimizeButton.Text = "─"
        end
    end)
    
    -- Drag functionality
    local function StartDrag()
        State.Dragging = true
        State.DragStart = Vector2.new(Mouse.X, Mouse.Y)
        State.DragObject = MainFrame
        
        local dragStartPosition = MainFrame.Position
        
        local connection
        connection = RunService.RenderStepped:Connect(function()
            if State.Dragging and State.DragObject then
                local delta = Vector2.new(Mouse.X, Mouse.Y) - State.DragStart
                MainFrame.Position = UDim2.new(
                    dragStartPosition.X.Scale,
                    dragStartPosition.X.Offset + delta.X,
                    dragStartPosition.Y.Scale,
                    dragStartPosition.Y.Offset + delta.Y
                )
            else
                connection:Disconnect()
            end
        end)
    end
    
    local function StopDrag()
        State.Dragging = false
        State.DragObject = nil
    end
    
    TopBar.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 then
            StartDrag()
        end
    end)
    
    UserInputService.InputEnded:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 then
            StopDrag()
        end
    end)
    
    return ScreenGui, MainFrame, ContentContainer, TabsContainer
end

-- Creare butoane pentru tab-uri
local function CreateTabs(tabsContainer, contentContainer)
    local tabs = {}
    local currentTab = nil
    
    local function CreateTabButton(name, icon)
        local tabButton = Instance.new("TextButton")
        tabButton.Name = name .. "Tab"
        tabButton.Text = icon .. " " .. name
        tabButton.Size = UDim2.new(0.25, 0, 1, 0)
        tabButton.Position = UDim2.new(#tabs * 0.25, 0, 0, 0)
        tabButton.BackgroundColor3 = Color3.fromRGB(40, 40, 50)
        tabButton.BackgroundTransparency = 0.5
        tabButton.TextColor3 = Color3.fromRGB(200, 200, 200)
        tabButton.Font = Enum.Font.Gotham
        tabButton.TextSize = 14
        tabButton.Parent = tabsContainer
        
        local tabCorner = Instance.new("UICorner")
        tabCorner.CornerRadius = UDim.new(0, 8)
        tabCorner.Parent = tabButton
        
        local tabStroke = Instance.new("UIStroke")
        tabStroke.Color = Color3.fromRGB(0, 170, 255)
        tabStroke.Thickness = 1
        tabStroke.Transparency = 0.8
        tabStroke.Parent = tabButton
        
        local tabContent = Instance.new("ScrollingFrame")
        tabContent.Name = name .. "Content"
        tabContent.Size = UDim2.new(1, 0, 1, 0)
        tabContent.Position = UDim2.new(0, 0, 0, 0)
        tabContent.BackgroundTransparency = 1
        tabContent.ScrollBarThickness = 3
        tabContent.ScrollBarImageColor3 = Color3.fromRGB(0, 170, 255)
        tabContent.Visible = false
        tabContent.Parent = contentContainer
        
        local uiListLayout = Instance.new("UIListLayout")
        uiListLayout.Padding = UDim.new(0, 10)
        uiListLayout.SortOrder = Enum.SortOrder.LayoutOrder
        uiListLayout.Parent = tabContent
        
        tabButton.MouseButton1Click:Connect(function()
            if currentTab then
                currentTab.Button.BackgroundColor3 = Color3.fromRGB(40, 40, 50)
                currentTab.Content.Visible = false
                TweenObject(currentTab.Button, {BackgroundTransparency = 0.5}, 0.2)
            end
            
            currentTab = tabs[name]
            currentTab.Content.Visible = true
            TweenObject(tabButton, {BackgroundColor3 = Color3.fromRGB(0, 120, 200), BackgroundTransparency = 0.2}, 0.2)
        end)
        
        tabs[name] = {
            Button = tabButton,
            Content = tabContent
        }
        
        return tabContent
    end
    
    -- Creare tab-uri
    local mainTab = CreateTabButton("Main", "⚙️")
    local visualsTab = CreateTabButton("Visuals", "👁️")
    local settingsTab = CreateTabButton("Settings", "⚡")
    local infoTab = CreateTabButton("Info", "ℹ️")
    
    -- Setează primul tab ca activ
    if tabs["Main"] then
        tabs["Main"].Button.BackgroundColor3 = Color3.fromRGB(0, 120, 200)
        tabs["Main"].Button.BackgroundTransparency = 0.2
        tabs["Main"].Content.Visible = true
        currentTab = tabs["Main"]
    end
    
    return tabs, mainTab, visualsTab, settingsTab, infoTab
end

-- Creare elemente UI
local function CreateUIElements(mainTab, visualsTab, settingsTab, infoTab)
    -- Main Tab Content
    local function CreateToggle(name, defaultValue, callback, parent)
        local toggleFrame = Instance.new("Frame")
        toggleFrame.Name = name .. "Toggle"
        toggleFrame.Size = UDim2.new(1, -20, 0, 50)
        toggleFrame.BackgroundColor3 = Color3.fromRGB(30, 30, 40)
        toggleFrame.BackgroundTransparency = 0.5
        toggleFrame.LayoutOrder = #parent:GetChildren()
        toggleFrame.Parent = parent
        
        local toggleCorner = Instance.new("UICorner")
        toggleCorner.CornerRadius = UDim.new(0, 8)
        toggleCorner.Parent = toggleFrame
        
        local toggleLabel = Instance.new("TextLabel")
        toggleLabel.Name = "Label"
        toggleLabel.Text = name
        toggleLabel.Size = UDim2.new(0.7, 0, 1, 0)
        toggleLabel.Position = UDim2.new(0.05, 0, 0, 0)
        toggleLabel.BackgroundTransparency = 1
        toggleLabel.TextColor3 = Color3.fromRGB(255, 255, 255)
        toggleLabel.Font = Enum.Font.Gotham
        toggleLabel.TextSize = 16
        toggleLabel.TextXAlignment = Enum.TextXAlignment.Left
        toggleLabel.Parent = toggleFrame
        
        local toggleButton = Instance.new("TextButton")
        toggleButton.Name = "ToggleButton"
        toggleButton.Text = ""
        toggleButton.Size = UDim2.new(0, 60, 0, 30)
        toggleButton.Position = UDim2.new(0.85, -30, 0.5, -15)
        toggleButton.BackgroundColor3 = defaultValue and Color3.fromRGB(0, 200, 100) or Color3.fromRGB(200, 50, 50)
        toggleButton.Parent = toggleFrame
        
        local toggleButtonCorner = Instance.new("UICorner")
        toggleButtonCorner.CornerRadius = UDim.new(1, 0)
        toggleButtonCorner.Parent = toggleButton
        
        local toggleCircle = Instance.new("Frame")
        toggleCircle.Name = "Circle"
        toggleCircle.Size = UDim2.new(0, 26, 0, 26)
        toggleCircle.Position = defaultValue and UDim2.new(1, -28, 0.5, -13) or UDim2.new(0, 2, 0.5, -13)
        toggleCircle.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
        toggleCircle.Parent = toggleButton
        
        local circleCorner = Instance.new("UICorner")
        circleCorner.CornerRadius = UDim.new(1, 0)
        circleCorner.Parent = toggleCircle
        
        local function UpdateToggle(value)
            if value then
                TweenObject(toggleButton, {BackgroundColor3 = Color3.fromRGB(0, 200, 100)}, 0.2)
                TweenObject(toggleCircle, {Position = UDim2.new(1, -28, 0.5, -13)}, 0.2)
            else
                TweenObject(toggleButton, {BackgroundColor3 = Color3.fromRGB(200, 50, 50)}, 0.2)
                TweenObject(toggleCircle, {Position = UDim2.new(0, 2, 0.5, -13)}, 0.2)
            end
            if callback then callback(value) end
        end
        
        toggleButton.MouseButton1Click:Connect(function()
            local newValue = not (toggleButton.BackgroundColor3 == Color3.fromRGB(0, 200, 100))
            UpdateToggle(newValue)
        end)
        
        UpdateToggle(defaultValue)
        
        return toggleFrame
    end
    
    -- Buton Auto Parry
    local autoParryToggle = CreateToggle("Auto Parry", Config.AutoParry, function(value)
        Config.AutoParry = value
        print("Auto Parry:", value and "ON" or "OFF")
    end, mainTab)
    
    -- Buton Visualizer
    local visualizerToggle = CreateToggle("Visualizer", Config.Visualizer, function(value)
        Config.Visualizer = value
        print("Visualizer:", value and "ON" or "OFF")
    end, visualsTab)
    
    -- Slider pentru distanță
    local function CreateSlider(name, minValue, maxValue, defaultValue, callback, parent)
        local sliderFrame = Instance.new("Frame")
        sliderFrame.Name = name .. "Slider"
        sliderFrame.Size = UDim2.new(1, -20, 0, 70)
        sliderFrame.BackgroundColor3 = Color3.fromRGB(30, 30, 40)
        sliderFrame.BackgroundTransparency = 0.5
        sliderFrame.LayoutOrder = #parent:GetChildren()
        sliderFrame.Parent = parent
        
        local sliderCorner = Instance.new("UICorner")
        sliderCorner.CornerRadius = UDim.new(0, 8)
        sliderCorner.Parent = sliderFrame
        
        local sliderLabel = Instance.new("TextLabel")
        sliderLabel.Name = "Label"
        sliderLabel.Text = name .. ": " .. defaultValue
        sliderLabel.Size = UDim2.new(1, -20, 0, 30)
        sliderLabel.Position = UDim2.new(0.05, 0, 0, 0)
        sliderLabel.BackgroundTransparency = 1
        sliderLabel.TextColor3 = Color3.fromRGB(255, 255, 255)
        sliderLabel.Font = Enum.Font.Gotham
        sliderLabel.TextSize = 16
        sliderLabel.TextXAlignment = Enum.TextXAlignment.Left
        sliderLabel.Parent = sliderFrame
        
        local sliderBar = Instance.new("Frame")
        sliderBar.Name = "Bar"
        sliderBar.Size = UDim2.new(1, -40, 0, 6)
        sliderBar.Position = UDim2.new(0.05, 0, 0.7, 0)
        sliderBar.BackgroundColor3 = Color3.fromRGB(60, 60, 70)
        sliderBar.Parent = sliderFrame
        
        local barCorner = Instance.new("UICorner")
        barCorner.CornerRadius = UDim.new(1, 0)
        barCorner.Parent = sliderBar
        
        local sliderFill = Instance.new("Frame")
        sliderFill.Name = "Fill"
        sliderFill.Size = UDim2.new((defaultValue - minValue) / (maxValue - minValue), 0, 1, 0)
        sliderFill.BackgroundColor3 = Color3.fromRGB(0, 170, 255)
        sliderFill.Parent = sliderBar
        
        local fillCorner = Instance.new("UICorner")
        fillCorner.CornerRadius = UDim.new(1, 0)
        fillCorner.Parent = sliderFill
        
        local sliderButton = Instance.new("TextButton")
        sliderButton.Name = "Button"
        sliderButton.Text = ""
        sliderButton.Size = UDim2.new(0, 20, 0, 20)
        sliderButton.Position = UDim2.new((defaultValue - minValue) / (maxValue - minValue), -10, 0.5, -10)
        sliderButton.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
        sliderButton.Parent = sliderBar
        
        local buttonCorner = Instance.new("UICorner")
        buttonCorner.CornerRadius = UDim.new(1, 0)
        buttonCorner.Parent = sliderButton
        
        local dragging = false
        
        local function UpdateSlider(value)
            local percentage = math.clamp((value - minValue) / (maxValue - minValue), 0, 1)
            TweenObject(sliderFill, {Size = UDim2.new(percentage, 0, 1, 0)}, 0.1)
            TweenObject(sliderButton, {Position = UDim2.new(percentage, -10, 0.5, -10)}, 0.1)
            sliderLabel.Text = name .. ": " .. string.format("%.2f", value)
            if callback then callback(value) end
        end
        
        sliderButton.InputBegan:Connect(function(input)
            if input.UserInputType == Enum.UserInputType.MouseButton1 then
                dragging = true
            end
        end)
        
        UserInputService.InputEnded:Connect(function(input)
            if input.UserInputType == Enum.UserInputType.MouseButton1 then
                dragging = false
            end
        end)
        
        sliderBar.InputBegan:Connect(function(input)
            if input.UserInputType == Enum.UserInputType.MouseButton1 then
                local relativeX = (input.Position.X - sliderBar.AbsolutePosition.X) / sliderBar.AbsoluteSize.X
                local value = minValue + (relativeX * (maxValue - minValue))
                UpdateSlider(value)
                dragging = true
            end
        end)
        
        UserInputService.InputChanged:Connect(function(input)
            if dragging and input.UserInputType == Enum.UserInputType.MouseMovement then
                local relativeX = (input.Position.X - sliderBar.AbsolutePosition.X) / sliderBar.AbsoluteSize.X
                local value = minValue + (math.clamp(relativeX, 0, 1) * (maxValue - minValue))
                UpdateSlider(value)
            end
        end)
        
        UpdateSlider(defaultValue)
        
        return sliderFrame
    end
    
    -- Slider pentru distanța de parry
    local distanceSlider = CreateSlider("Parry Distance", 0.1, 1.0, Config.ParryDistance, function(value)
        Config.ParryDistance = value
    end, settingsTab)
    
    -- Info Tab Content
    local infoLabel = Instance.new("TextLabel")
    infoLabel.Name = "InfoLabel"
    infoLabel.Text = [[⚔️ NoEnemies Hub ⚔️

Version: 2.0
Developer: Scripting Team
Game: Blade Ball

Features:
• Auto Parry System
• Visual Effects
• Customizable Settings
• Modern GUI

Keybind: Right Shift
]]
    infoLabel.Size = UDim2.new(1, -20, 0, 300)
    infoLabel.Position = UDim2.new(0, 10, 0, 10)
    infoLabel.BackgroundTransparency = 1
    infoLabel.TextColor3 = Color3.fromRGB(255, 255, 255)
    infoLabel.Font = Enum.Font.Gotham
    infoLabel.TextSize = 14
    infoLabel.TextYAlignment = Enum.TextYAlignment.Top
    infoLabel.Parent = infoTab
    
    -- Buton de execuție script
    local executeButton = Instance.new("TextButton")
    executeButton.Name = "ExecuteButton"
    executeButton.Text = "🚀 Execute Script"
    executeButton.Size = UDim2.new(1, -40, 0, 50)
    executeButton.Position = UDim2.new(0, 20, 0, 360)
    executeButton.BackgroundColor3 = Color3.fromRGB(0, 170, 255)
    executeButton.BackgroundTransparency = 0.3
    executeButton.TextColor3 = Color3.fromRGB(255, 255, 255)
    executeButton.Font = Enum.Font.GothamBold
    executeButton.TextSize = 16
    executeButton.Parent = ContentContainer
    
    local executeCorner = Instance.new("UICorner")
    executeCorner.CornerRadius = UDim.new(0, 10)
    executeCorner.Parent = executeButton
    
    executeButton.MouseButton1Click:Connect(function()
        TweenObject(executeButton, {BackgroundTransparency = 0.7}, 0.1)
        wait(0.1)
        TweenObject(executeButton, {BackgroundTransparency = 0.3}, 0.1)
        
        -- Încarcă scriptul extern
        loadstring(game:HttpGet("https://scriptblox.com/raw/UPD-Blade-Ball-op-autoparry-with-visualizer-8652"))()
        CreateNotification("NoEnemiesHub", "External Script Loaded Successfully!", "rbxassetid://135351041318579", 5)
    end)
end

-- Funcția principală de inițializare
local function Initialize()
    wait(1)
    
    -- Notificare inițială
    CreateNotification("NoEnemiesHub", "Auto Parry GUI Loaded Successfully!", "rbxassetid://135351041318579", 5)
    
    -- Creare GUI
    local screenGui, mainFrame, contentContainer, tabsContainer = CreateGUI()
    screenGui.Parent = Player.PlayerGui
    
    -- Creare tab-uri
    local tabs, mainTab, visualsTab, settingsTab, infoTab = CreateTabs(tabsContainer, contentContainer)
    
    -- Creare elemente UI
    CreateUIElements(mainTab, visualsTab, settingsTab, infoTab)
    
    -- Setup Auto Parry System
    SetupAutoParry()
    
    -- Keybind pentru toggle GUI
    UserInputService.InputBegan:Connect(function(input, gameProcessed)
        if not gameProcessed and input.KeyCode == Config.Keybind then
            State.GUIVisible = not State.GUIVisible
            if State.GUIVisible then
                TweenObject(mainFrame, {Size = UDim2.new(0, 400, 0, 450), Position = UDim2.new(0.5, -200, 0.5, -225)}, 0.3)
            else
                TweenObject(mainFrame, {Size = UDim2.new(0, 0, 0, 0), Position = UDim2.new(0.5, 0, 0.5, 0)}, 0.3)
            end
        end
    end)
    
    -- Animare de intrare
    mainFrame.Size = UDim2.new(0, 0, 0, 0)
    mainFrame.Position = UDim2.new(0.5, 0, 0.5, 0)
    TweenObject(mainFrame, {Size = UDim2.new(0, 400, 0, 450), Position = UDim2.new(0.5, -200, 0.5, -225)}, 0.5, Enum.EasingStyle.Back, Enum.EasingDirection.Out)
    
    print("🎮 NoEnemies Hub GUI Initialized!")
    print("📌 Press Right Shift to toggle GUI")
end

-- Start
Initialize()
